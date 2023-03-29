from flask import Flask, request, send_file, Response, jsonify
from io import BytesIO
from flask_cors import CORS
from base64 import b64encode

from PIL import Image
import numpy as np
from tf_inference import TFInference

from pymongo import MongoClient

app = Flask(__name__)
# Allow access from any origin for any of the routes by default
cors = CORS(app)

mongo_client = MongoClient("mongodb://mongodb-rs-service:27017/")
db = mongo_client["test"]

MIME_TYPE_TO_PIL_TYPE = {'image/png': 'PNG', 'image/jpeg': 'JPEG'}

# Initialize the TFInference module.
tf_inference_module = TFInference()

# Route the index page
@app.route('/')
def index():
    elements_from_db = str(db["test"].find_one())
    return 'Hello! ' + elements_from_db

@app.route('/predict', methods=['POST'])
def predict():
    request_img = request.files['image']
    input_img = Image.open(request_img)

    # Run the TF model on the input image.
    preds_img = tf_inference_module.predict(input_img)

    # Base64 encode the image before sending it as a response.
    output = BytesIO()
    preds_img.save(output, format=MIME_TYPE_TO_PIL_TYPE[request_img.mimetype])
    img_b64 = b64encode(output.getvalue()).decode("utf-8")

    return jsonify({'status': True, 'predictions': img_b64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)