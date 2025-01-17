from pymongo import MongoClient
import random
import string
from datetime import datetime

from DB import DB

db = DB()

friends = db.friends


def integrity():
    # usersDBから全ユーザーのuidを取得
    uids = []
    for user in db.users.find():
        uids.append(user["uid"])

    # friendsDBにuidを追加
    for uid in uids:
        # friendsDBにuidが存在しない場合、uidを追加
        if not friends.find_one({"uid": uid}):
            print("uid not found in friendsDB" + uid)
            friends.insert_one({"uid": uid, "friends": []})

    # userDBに存在しないuidを削除
    for friend in friends.find():
        if friend["uid"] not in uids:
            print("uid not found in usersDB" + friend["uid"])
            friends.delete_one({"uid": friend["uid"]})


def add_friend(uid, friend_uid):
    # 自分をフレンドに追加しようとしている場合、エラー
    if uid == friend_uid:
        print("cannot add yourself as a friend")
        return False

    # uidが存在しない場合、エラー
    if not friends.find_one({"uid": uid}):
        if db.users.find_one({"uid": uid}):
            integrity()
        else:
            print("uid not found")
            return False
    # フレンドがすでに存在する場合、エラー
    if friends.find_one({"uid": uid, "friends": friend_uid}):
        print("friend already exists")
        return False

    # frined_uidの有効性を確認
    if not friends.find_one({"uid": friend_uid}):
        if db.users.find_one({"uid": friend_uid}):
            integrity()
        else:
            print("friend_uid not found")
            return False

    # フレンドのuidを追加
    friends.update_one({"uid": uid}, {"$push": {"friends": friend_uid}})

    # 相手の方にも自分のuidを追加
    friends.update_one({"uid": friend_uid}, {"$push": {"friends": uid}})


def remove_friend(uid, friend_uid):
    # uidが存在しない場合、エラー
    if not friends.find_one({"uid": uid}):
        print("uid not found")
        return False
    # フレンドが存在しない場合、エラー
    if not friends.find_one({"uid": uid, "friends": friend_uid}):
        print("friend not found")
        return False

    # frined_uidの有効性を確認
    if not friends.find_one({"uid": friend_uid}):
        print("friend_uid not found")
        return False

    # フレンドのuidを削除
    friends.update_one({"uid": uid}, {"$pull": {"friends": friend_uid}})

    # 相手側から自分を削除
    friends.update_one({"uid": friend_uid}, {"$pull": {"friends": uid}})


def get_friends(uid):
    # uidが存在しない場合、エラー
    if not friends.find_one({"uid": uid}):
        print("uid not found")

        # 整合性が取れていないので，応急処置
        return []

    users = fetch_users()
    res = []
    for friend_uid in friends.find_one({"uid": uid})["friends"]:
        if friend_uid in users:
            res.append(users[friend_uid])

    # フレンドのuidを取得
    return res


def fetch_users():
    """
    usersを取得する

    :return users: list[dict]
    """

    data = db.users.find()
    res = {row["uid"]: {"uid": row["uid"], "name": row["name"], "name_id": row["name_id"]}
           for row in data}
    return res


def generate_qr_data(uid: str, name: str) -> str:
    """
    QRコードのデータを生成する
    20文字の乱数 + ユーザー名

    :param str uid: ユーザーID
    :param str name: ユーザー名
    :return: QRコードのデータ
    """

    code = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=20))
    data = code + ',' + name

    current_time = datetime.now()

    db.qr_data.insert_one({
        'uid': uid,
        'code': code,
        'timestamp': current_time
    })

    return data
