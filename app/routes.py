
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, Organization, Cluster, Deployment
from app.scheduler import push_to_queue
from werkzeug.security import generate_password_hash, check_password_hash
import redis
from app import mongo

bp = Blueprint('bp', __name__)
redis_client = redis.StrictRedis.from_url("redis://localhost:6379/0")

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    org_id   = data['organization_id']
    password_hash = generate_password_hash(password)

    # Check if the username exists
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"msg": "User already exists"}), 400

    user = User(username, password_hash, org_id, 'developer')
    mongo.db.users.insert_one(user.__dict__)

    return jsonify({"msg": "User created successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = mongo.db.users.find_one({"username": username})
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    print("user : ", user, type(user))
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({access_token:access_token})

@bp.route('/clusters/create', methods=['POST'])
@jwt_required()
def create_cluster():
    current_user = get_jwt_identity()
    data = request.get_json()

    cluster = Cluster(data['name'], data['cpu'], data['ram'], data['gpu'])
    cluster.create_cluster()

    return jsonify({"msg": "Cluster created successfully"}), 201

@bp.route("/clusters", methods=["GET"])
@jwt_required()
def list_clusters():
    clusters = list(mongo.db.clusters.find())
    for cluster in clusters:
        cluster["_id"] = str(cluster["_id"])
    return jsonify(clusters)

@bp.route('/deployments', methods=['POST'])
@jwt_required()
def create_deployment():
    current_user = get_jwt_identity()
    data = request.get_json()

    deployment = Deployment(current_user, data['cluster_name'], data['image_path'], 
                            data['priority'], data['required_cpu'], 
                            data['required_ram'], data['required_gpu'])
    
    inserted_id = deployment.create_deployment()
    print("inserted_id : ", str(inserted_id))
    # redis_client.rpush('deployment_queue', str(inserted_id))
    push_to_queue({str(inserted_id): data['priority']})

    return jsonify({"msg": "Deployment created and queued"}), 201

@bp.route('/deployments/queue', methods=['GET'])
def get_queue():
    queue = redis_client.zrange("deployment_queue", 0, -1, withscores=True)
    # response = []
    # for item in queue:

    print("queue : ", queue)
    return jsonify({"queue": queue}), 200
