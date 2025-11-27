from flask_restful import Resource
from flask import request, jsonify, make_response
from user_datastore import user_datastore
from werkzeug.security import check_password_hash, generate_password_hash
from flask_security import utils, auth_token_required, roles_required
from database import db

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            result = {
                'message' : 'Email and password are required.'
            }
            return make_response(jsonify(result), 400)
        
        email = data.get('email')
        password = data.get('password')

        if user_datastore.find_user(email=email):
            result = {
                'message' : 'User with this email already exists.'
            }
            return make_response(jsonify(result), 409)
        
        user_role = user_datastore.find_role('user')
        user_datastore.create_user(email=email, password=generate_password_hash(password), roles = [user_role])

        db.session.commit()

        response = {
            'message': 'Login successful.',
            'user_details': {
                'email': email,
                'roles': [user_role.name]
            },
        }
        return make_response(jsonify(response), 201)

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            result = {
                'message' : 'Email and password are required.'
            }
            return make_response(jsonify(result), 400)
        
        email = data.get('email')
        password = data.get('password')

        user = user_datastore.find_user(email=email)

        if not user:
            result = {
                'message' : 'User not found.'
            }
            return make_response(jsonify(result), 404)
        
        if not check_password_hash(user.password, password):
            result = {
                'message' : 'Invalid password.'
            }
            return make_response(jsonify(result), 401)
        
        auth_token = user.get_auth_token()

        utils.login_user(user)

        response = {
            'message': 'Login successful.',
            'user_details': {
                'email': user.email,
                'roles': [role.name for role in user.roles],
                'auth_token': auth_token
            }
        }
        return make_response(jsonify(response), 200)
    
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        result = {
            'message': 'Logout successful.'
        }
        return make_response(jsonify(result), 200)
        