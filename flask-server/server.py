from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
import jwt

from services.users import users_service

from io import BytesIO
from base64 import b64encode
import hashlib

from PIL import Image
import numpy as np
from tf_inference import TFInference

import pymongo

import redis

app = Flask(__name__)
app.register_blueprint(users_service)
# Allow access from any origin for any of the routes by default.
cors = CORS(app)

# Setup JSON Web Tokens
app.config['JWT_SECRET_KEY'] = 'cebbfc54440208cbe8b35466bc5263db'
jwt = JWTManager(app)

# Connect to the MongoDB service running in Kubernetes if the 
# flask-server is running in the Kubernetes cluster on GCP. Else,
# when run locally, mongo_client is just set to None.
mongo_client = pymongo.MongoClient("mongodb://mongodb-rs-service:27017/")
try:
    mongo_client.server_info()
except pymongo.errors.ServerSelectionTimeoutError:
    print('Unable to connect to the MongoDB service')
    mongo_client = None

# Connect to the Redis MemoryStore instance running in GCP if the 
# flask-server is running in the Kubernetes cluster on GCP. Else,
# when run locally, redis_client is just set to None.
redis_client = redis.Redis(host='10.60.49.244', port=6379, db=0)
try:
    redis_client.ping()
except redis.ConnectionError:
    print('Unable to connect to the Redis service')
    redis_client = None

MIME_TYPE_TO_PIL_TYPE = {'image/png': 'PNG', 'image/jpeg': 'JPEG'}

# Initialize the TFInference module.
tf_inference_module = TFInference()

# Redis cache methods
def _get_redis_key(api_route, id):
    return api_route + '::' + id

def get_from_cache(api_route, id):
    if not redis_client:
        return None

    redis_key = _get_redis_key(api_route, id)
    if redis_client.exists(redis_key):
        return redis_client.get(redis_key).decode("utf-8")
    else:
        return None

def add_to_cache(api_route, id, value):
    if not redis_client:
        return False
    
    redis_key = _get_redis_key(api_route, id)
    redis_client.setex(redis_key, 300, value)
    return True

# Setup a custom error message that is displayed when a token passed in the headers
# is either absent or invalid.
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": 'Invalid token!'}), 401

# Setup a custom error message that is displayed when a token passed in the headers
# has expired.
@jwt.expired_token_loader
def my_expired_token_callback(header, payload):
    return jsonify({"message": 'Token has expired!'}), 401

# Route the index page
@app.route('/')
def index():
    if mongo_client:
        elements_from_db = str(mongo_client["test"]["test"].find_one())
    else:
        elements_from_db = ''
    return 'Hello! ' + elements_from_db

@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    # Get the current user from the JSON Web Token.
    current_user = get_jwt_identity()

    if 'image' not in request.files:
        return jsonify({'status': False, 'username': current_user, 'message': 'image not present in the request'})

    request_img = request.files['image']
    input_img = Image.open(request_img)

    # Compute a Base64 encoding of the image to check the cache.
    input_bytes = BytesIO()
    input_img.save(input_bytes, format=MIME_TYPE_TO_PIL_TYPE[request_img.mimetype])
    input_img_b64 = b64encode(input_bytes.getvalue()).decode("utf-8")
    md5_input_img = hashlib.md5(input_img_b64.encode('utf-8')).hexdigest()

    # Try to see if the image is already present in the cache. If it is, return preds from
    # the cache directly.
    preds_from_cache = get_from_cache('predict', md5_input_img)
    if preds_from_cache:
        return jsonify({'status': True, 'cacheHit': True, 'username': current_user, 'predictions': preds_from_cache})

    # Run the TF model on the input image.
    preds_img = tf_inference_module.predict(input_img)

    # Base64 encode the prediction image to send in the response.
    preds_bytes = BytesIO()
    preds_img.save(preds_bytes, format=MIME_TYPE_TO_PIL_TYPE[request_img.mimetype])
    preds_img_b64 = b64encode(preds_bytes.getvalue()).decode("utf-8")

    # Add input image and predictions to the cache.
    add_to_cache('predict', md5_input_img, preds_img_b64)

    return jsonify({'status': True, 'cacheHit': False, 'username': current_user, 'predictions': preds_img_b64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)