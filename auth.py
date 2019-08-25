from functools import wraps

import bcrypt
from flask import redirect, request

from storage import StorageType, StorageFactory


def authenticate(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not('admin_auth_token' in request.cookies):
            return redirect('/admin/login')

        auth_token = request.cookies['admin_auth_token']
        s = _get_storage()
        correct_token = s.get_blob('login_token').encode('UTF-8')

        if auth_token != correct_token:
            return redirect('/admin/login')

        return func(*args, **kwargs)
    return inner


def _get_storage():
    return StorageFactory.create(StorageType.S3)

def _check_password(password) -> bool:
    s = _get_storage()
    good_hash = s.get_blob("password")
    return bcrypt.checkpw(password, good_hash)
