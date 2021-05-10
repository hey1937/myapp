# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import request, session
# 自定义key
key = "my_key%my_key"


def generate_access_token(mobile: str = "", algorithm: str = 'HS256', exp: float = 2):
    """
    生成access_token
    :param mobile: 获取的手机号
    :param algorithm:加密算法
    :param exp:过期时间
    :return:token
    """

    now = datetime.utcnow()
    exp_datetime = now + timedelta(hours=exp)
    access_payload = {
        'exp': exp_datetime,
        'flag': 0,
        'iat': now,
        'iss': 'qin',
        'mobile': mobile
    }
    access_token = jwt.encode(access_payload, key, algorithm=algorithm)
    return access_token,exp_datetime


def generate_refresh_token(mobile: str = "", algorithm: str = 'HS256', fresh: float = 30):
    """
    生成refresh_token

    :param mobile: 获取的手机号
    :param algorithm:加密算法
    :param fresh:过期时间
    :return:token
    """
    now = datetime.utcnow()
    # 刷新时间为30天
    exp_datetime = now + timedelta(days=fresh)
    refresh_payload = {
        'exp': exp_datetime,
        'flag': 1,
        'iat': now,
        'iss': 'qin',
        'mobile': mobile
    }

    refresh_token = jwt.encode(refresh_payload, key, algorithm=algorithm)
    return refresh_token

def decode_auth_token(token: str):
    """
    解密token
    :param token:token字符串
    :return:
    """
    try:
        # 取消过期时间验证
        # payload = jwt.decode(token, key, options={'verify_exp': False})
        payload = jwt.decode(token, key=key)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
        return ""
    else:
        return payload

def identify(auth_header: str):
    """
    用户鉴权
    :return:
    """
    if auth_header:
        payload = decode_auth_token(auth_header)
        if not payload:
            return False
        if "mobile" in payload and "flag" in payload:
            if payload["flag"] == 1:
                # 用来获取新access_token的refresh_token无法获取数据
                return False
            elif payload["flag"] == 0:
                return payload["mobile"]
            else:
                # 其他状态暂不允许
                return False
        else:
            return False
    else:
        return False


def login_required(f):
    """
    登陆保护，验证用户是否登陆
    :param f:
    :return:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", default=None)
        if not token:
            return "请登陆"
        mobile = identify(token)
        if not mobile:
             return "请登陆"
        # 获取到用户并写入到session中,方便后续使用
        session["mobile"] = mobile
        return f(*args, **kwargs)
    return wrapper
