from flask import Blueprint, request, jsonify
from DB import DB
import datetime

from Friend import manageFriend

FRIEND_BP = Blueprint('friend', __name__, url_prefix='/friend')

# MongoDBに接続
db = DB()


@FRIEND_BP.route('/add', methods=['POST'])
def add_friend():
    if not 'token' in request.json:
        return jsonify({'error': 'Missing token'}), 400
    req_token = request.json['token']

    if not 'users' in request.json:
        return jsonify({'error': 'User not defined'}), 400
    req_users = request.json['users']

    if not req_users:
        return jsonify({'error': 'User not defined'}), 400

    for user in req_users:
        if not 'name' in user:
            return jsonify({'error': 'UserName not defined'}), 400
        if not 'id' in user:
            return jsonify({'error': 'UserID not defined'}), 400

        uid = db.users.find_one({'token': req_token})
        if not uid:
            return jsonify({'error': 'Invalid token'}), 400
        uid = uid['uid']

        friend_uid = db.users.find_one(
            {'name': user['name'], 'name_id': user['id']})
        if not friend_uid:
            return jsonify({'error': 'User not found'}), 400
        friend_uid = friend_uid['uid']

        manageFriend.add_friend(uid, friend_uid)

    return jsonify({'message': 'Success'}), 200


@FRIEND_BP.route('/get', methods=['POST'])
# TODO: getだけどPOSTでいいのか？
def get_friend():
    if not 'token' in request.json:
        return jsonify({'error': 'Missing token'}), 400
    req_token = request.json['token']

    uid = db.users.find_one({'token': req_token})
    if not uid:
        return jsonify({'error': 'Invalid token'}), 400
    uid = uid['uid']

    friends = manageFriend.get_friends(uid)

    return jsonify({'friends': friends}), 200


@FRIEND_BP.route('/delete', methods=['POST'])
def delete_friend():
    if not 'token' in request.json:
        return jsonify({'error': 'Missing token'}), 400
    req_token = request.json['token']

    if not 'users' in request.json:
        return jsonify({'error': 'User not defined'}), 400
    req_users = request.json['users']

    if not req_users:
        return jsonify({'error': 'User not defined'}), 400

    for user in req_users:
        if 'name' not in user:
            return jsonify({'error': 'UserName not defined'}), 400
        if 'id' not in user:
            return jsonify({'error': 'UserID not defined'}), 400

        uid = db.users.find_one({'token': req_token})
        if not uid:
            return jsonify({'error': 'Invalid token'}), 400
        uid = uid['uid']

        friend_uid = db.users.find_one(
            {'name': user['name'], 'name_id': user['id']})
        if not friend_uid:
            return jsonify({'error': 'User not found'}), 400
        friend_uid = friend_uid['uid']

        manageFriend.remove_friend(uid, friend_uid)

    return jsonify({'message': 'Success'}), 200


@FRIEND_BP.route('/fetch_qr_data', methods=['POST'])
def fetch_qr_data():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400

    user = db.users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    data = manageFriend.generate_qr_data(uid=user['uid'], name=user['name'])
    return jsonify({'data': data}), 200


@FRIEND_BP.route('/add_request', methods=['POST'])
def add_request():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    code = request.json['code']
    if not code:
        return jsonify({'error': 'Missing code'}), 400

    user = db.users.find_one({'token': token})
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    # 5分以内のQRコードのみ有効
    # 5分以上経過しているデータをqr_dataから削除する
    db.qr_data.delete_many(
        {'timestamp': {'$lt': datetime.datetime.now() - datetime.timedelta(minutes=5)}})

    qr_data = db.qr_data.find_one({'code': code})
    if not qr_data:
        return jsonify({'error': 'Invalid code'}), 400

    manageFriend.add_friend(uid=user['uid'], friend_uid=qr_data['uid'])
    return jsonify({'done': 'success'}), 200


@FRIEND_BP.route('/delete_request', methods=['POST'])
def delete_request():
    token = request.json['token']
    if not token:
        return jsonify({'error': 'Missing token'}), 400
    friend_uid = request.json['friend_uid']
    if not friend_uid:
        return jsonify({'error': 'Missing friend_uid'}), 400
    name_id = request.json['name_id']
    if not name_id:
        return jsonify({'error': 'Missing name_id'}), 400

    req_user = db.users.find_one({'token': token})
    if not req_user:
        return jsonify({'error': 'Invalid token'}), 400

    friend = db.users.find_one({'name_id': name_id, 'uid': friend_uid})
    if not friend:
        return jsonify({'error': 'Invalid friend_uid, name_id'}), 400

    manageFriend.remove_friend(uid=req_user['uid'], friend_uid=friend_uid)
    return jsonify({'done': 'success'}), 200
