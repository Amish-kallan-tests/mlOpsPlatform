import os

class Config:
    MONGO_URI = "mongodb://mongo:27017/mlops"
    REDIS_URL = "redis://redis:6379/0"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
