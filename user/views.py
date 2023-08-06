from application import api, mongo
from flask import Blueprint , jsonify, make_response , request
from flask_restful import Resource
import uuid
import time
import bcrypt

User = Blueprint("user", __name__)  # create Blueprint
users_collection = mongo['users_collection']

#Add user and get all user
class Register_User(Resource):
    def get(self):
        all_users_data = list(users_collection.find({}, {"_id": 0, "password": 0}))
        if all_users_data:
                    return all_users_data
    def post(self):
        try:
            data = request.json
            password = data["password"].encode()
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))
            data["email"] = str(uuid.uuid4().hex)[:10] + str(round(time.time()))
            data["password"] = hashed_password
            users_collection.insert_one(data)
            return {'message': 'User created', 'email': data["email"]}, 201
        except Exception as e:
            return make_response(
                jsonify(
                    {
                        "message": "Something went wrong",
                        "Exception": str(e),
                    }
                ),
                500,
            )
class Update_User(Resource):
    def get(self , email = None):
        try:
            
            if email:
                user_data = users_collection.find_one({"email": email}, {"_id": 0, "password": 0})

                if user_data:
                    return user_data
                else:
                    return make_response(jsonify({"message": "User not found"}), 404)
            
        except Exception as e:
            return make_response(jsonify({"message": "Something went wrong", "Exception": str(e)}), 500)
        
    
        
    def put(self, email=None):
        if email is None:
            return make_response(jsonify({"message": "email can not empty"}), 403)            
        data = request.json
        result = users_collection.update_one({'email': email}, {'$set': data})
        if result.modified_count > 0:
            return make_response(jsonify({'message': 'User updated'}), 200)
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)
        
    def delete(self , email = None):
        result = users_collection.delete_one({'email': email})
        if result.deleted_count > 0:
            return make_response(jsonify({'message': 'User deleted'}), 200)
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)

class Login(Resource):
    def post(self):
        try:
            data = request.json
            user = users_collection.find_one({"email": data["username"]})
            if user and bcrypt.checkpw(data["password"].encode(), user["password"]):
                response = make_response(
                    jsonify({"message": "Login successful", "email": user["email"]}), 200
                )

                #Not working 
                # response.set_cookie("email", user["email"], expires=1000)  # Set the cookie to expire after 7 days
                return response
                # return {"message": "Login successful", "email": user["email"]}, 200
            else:
                return {"message": "Invalid credentials"}, 401
        except Exception as e:
            return make_response(
                jsonify({"message": "Something went wrong", "Exception": str(e)}), 500
            )

class Logout(Resource):
    def post(self):
        # Perform any logout-related tasks, such as invalidating session tokens or clearing session data.
        # For simplicity, we'll just return a logout message.
        return {"message": "Logout successful"}, 200

api.add_resource(Update_User, "/users/<string:email>")
api.add_resource(Register_User , "/users")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")