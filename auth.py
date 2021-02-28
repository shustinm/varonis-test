import json
import hashlib
import sanic
from base64 import b64encode
from sanic_jwt import exceptions

# Generated once with os.urandom(32)
# it's better to generate salt during runtime and store with the password, but this will suffice for now.
SALT = b'y\x03\xc40\x07\xcf\x84tt\xd2"\x06\x8by\xe6\x94T\x1f\x1f\xa0\xff\x11\x8a\xc2?\xf1\xd4\x96\xafVd^'
USER_FILE = 'users.json'


def hash_password(password: str):
    return hashlib.pbkdf2_hmac(hash_name='sha256', salt=SALT, iterations=100000,
                               password=password.encode('utf-8'))


# noinspection PyShadowingNames, PyUnresolvedReferences
def authenticate(request: sanic.request.Request):
    """
    Returns the user if the authentication was successful, otherwise raises a sanic_jwt.exception

    Passwords are saved hashed by `hash_password` and encoded in base64 in a JSON file.
    """

    # Get username and password from json
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    # Load users from json
    with open(USER_FILE, 'r') as f:
        users = json.load(f)['users']

    username_table = {u['username']: u for u in users}

    if username not in username_table:
        raise exceptions.AuthenticationFailed("User not found.")

    user = username_table[username]

    # Hash the given password and encode to compare with saved password
    if b64encode(hash_password(password)) != user['password'].encode():
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user


if __name__ == '__main__':
    from types import SimpleNamespace
    request = SimpleNamespace(json={'username': 'michael', 'password': '123'})
    authenticate(request)