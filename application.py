from flask import Flask, jsonify
from flask_restful import Api
import os
from pymongo import MongoClient
from flask_cors import CORS  
from common.extentions import jwt
from flask_jwt_extended import JWTManager

app = Flask(__name__)


app.config["MONGO_URI"] = os.environ.get("DATABASE_URL")
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

CORS(app, origins=["http://localhost:8000"])


api = Api(app)
mongo_client = MongoClient(app.config["MONGO_URI"])

mongo = mongo_client["BiPolar"]

# creating another flask app to handle /favicon.ico redirects and tracebacks
ping_app = Flask(__name__)

@ping_app.route('/', methods=['GET'])
def ping():
    return jsonify({'Ping Hello!': 'World!'})

