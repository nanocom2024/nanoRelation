import hashlib
from DB import DB

db = DB()
device_keys = db.device_keys


def generate_major_minor(public_key: str) -> tuple[str, str]:
    """
    majorとminorをpublic_keyから生成する

    :param str public_key:
    :return major, minor: (str, str)
    """

    temp = public_key
    while True:
        major, minor = generate(temp)
        device_key = device_keys.find_one({'major': major, 'minor': minor})
        if not device_key:
            break
        temp = hashlib.sha256(temp.encode()).hexdigest()

    return str(major), str(minor)


def generate(key: str) -> tuple[int, int]:
    forward = key[:32]
    backward = key[32:]

    forward_hash = hashlib.sha256(forward.encode()).hexdigest()
    backward_hash = hashlib.sha256(backward.encode()).hexdigest()

    # 16bitのuintに変換
    major = int(forward_hash, 16) % 2**16
    minor = int(backward_hash, 16) % 2**16

    return major, minor


def fetch_pairings() -> list[dict]:
    """
    pairingsを取得する

    :return pairings: list[dict]
    """

    data = db.pairings.find()
    res = [{"uid": row["uid"], "major": row["major"], "minor": row["minor"]}
           for row in data]
    return res


if __name__ == '__main__':
    public_key = 'a' * 64
    print(generate(public_key))
    # (42311, 42311)
