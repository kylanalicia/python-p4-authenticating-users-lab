#!/usr/bin/env python3

from flask import Flask, request, jsonify, session
from flask_restful import Api, Resource

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
api = Api(app)

# Sample user data (you can replace this with your own user data)
users = [{'id': 1, 'username': 'user1'}, {'id': 2, 'username': 'user2'}]

# Resource for user login
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        
        # Find the user by username (assuming usernames are unique)
        user = next((user for user in users if user['username'] == username), None)

        if user:
            session['user_id'] = user['id']
            return jsonify(user), 200
        else:
            return '', 401

# Resource for user logout
class LogoutResource(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id')
        return '', 204

# Resource for checking the session
class CheckSessionResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        
        if user_id is not None:
            user = next((user for user in users if user['id'] == user_id), None)
            if user:
                return jsonify(user), 200
        
        return '', 401

api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(CheckSessionResource, '/check_session')

if __name__ == '__main__':
    app.run(debug=True)
