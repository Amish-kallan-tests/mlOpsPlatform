from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
import redis

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mongo.init_app(app)
    jwt.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)

    return app
