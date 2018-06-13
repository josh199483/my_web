import time
import json
from functools import wraps
from flask import abort, render_template
from flask_login import current_user

# 符合我們網頁的權限管理
def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*pos_args,**kw_args):
            if not current_user.can(permission):
                abort(403)
            return func(*pos_args,**kw_args)
        return decorated_function
    return decorator

# admin的decorator  
def admin_required(func):
    permission = 'admin'
    return permission_required(permission)(func)


# 2018/3/27，Joshua，自定義的序列化類別 decorator
class CustomizedJsonSerializer:
    def __init__(self, serializeType):
        self._serializeType = serializeType

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            serializer = lambda x: x.__str__() if isinstance(x, self._serializeType) else None
            serializedData = json.dumps(res, default=serializer)
            return serializedData
        return wrapper