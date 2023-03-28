from flask import Flask
from flask_cors import CORS

from pymongo import MongoClient

app = Flask(__name__)
# Allow access from any origin for any of the routes by default
cors = CORS(app)

mongo_client = MongoClient("mongodb://mongodb-rs-service:27017/")
db = mongo_client["test"]

# Route the index page
@app.route('/')
def index():
    elements_from_db = str(db["test"].find_one())
    return 'Hello! ' + elements_from_db

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)