from flask import Blueprint, request, jsonify
from DB import DB

FRIEND_BP = Blueprint('friend', __name__, url_prefix='/friend')

# MongoDBに接続
db = DB()

@FRIEND_BP.route('/add', methods=['POST'])
def add_friend():
    token = request.json['token']
    if not token: return jsonify({'error': 'Missing token'}), 400
    
    users = request.json['Users']
    if not users: return jsonify({'error': 'User not defined'}), 400

    for user in users:
        if not user['name']: return jsonify({'error': 'UserName not defined'}), 400
        if not user['id']: return jsonify({'error': 'UserID not defined'}), 400

@FRIEND_BP.route('/get', methods=['POST'])
def add_friend():
    token = request.json['token']
    if not token: return jsonify({'error': 'Missing token'}), 400

@FRIEND_BP.route('/delete', methods=['POST'])
def add_friend():
    token = request.json['token']
    if not token: return jsonify({'error': 'Missing token'}), 400

    users = request.json['Users']
    if not users: return jsonify({'error': 'User not defined'}), 400

    for user in users:
        if not user['name']: return jsonify({'error': 'UserName not defined'}), 400
        if not user['id']: return jsonify({'error': 'UserID not defined'}), 400