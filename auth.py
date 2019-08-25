import base64
from functools import wraps
import os
from typing import Dict, Any

import bcrypt
from flask import redirect, request
from flask_json import json_response

from storage import StorageType, StorageFactory


def authenticate(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not('admin_auth_token' in request.cookies):
            return redirect('/admin/login')

        auth_token = request.cookies['admin_auth_token']
        s = _get_storage()
        correct_token = s.get_blob('login_token').decode('utf8')

        if auth_token != correct_token:
            return redirect('/admin/login')

        return func(*args, **kwargs)
    return inner


def get_login_token(data: Dict[str, Any]):
    password = data["password"]
    if not _check_password(password):
        return json_response(
            ok=False, err="The password entered is incorrect", status=401
        )

    s = _get_storage()
    token = base64.b64encode(os.urandom(32))
    s.put_blob('login_token', token)

    return json_response(ok=True, token=token.decode('utf8'))


def _get_storage():
    return StorageFactory.create(StorageType.S3)

def _check_password(password: str) -> bool:
    s = _get_storage()
    good_hash = s.get_blob("password")
    return bcrypt.checkpw(bytes(password, "utf8"), good_hash)
