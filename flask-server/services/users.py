from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import datetime

users_service = Blueprint('users_service', __name__)

@users_service.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth:
        return jsonify({'message': 'Authorization not set in the request'}), 401

    if auth and auth.username and auth.password == 'password':
        # Create an access token that is valid for 5 minutes.
        access_token = create_access_token(identity=auth.username, expires_delta=datetime.timedelta(minutes=5))
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid username and/or password!'}), 401
