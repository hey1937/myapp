# -*- coding:utf-8 -*-
from flask import Flask, jsonify,abort
from flask import request
from util import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python_dev_user:2Y6eEnp4bAFXNuVh8Tj7@116.62.205.226:3306/trans_tools?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
db.init_app(app)


class User(db.Model):
    #声明表名
    __tablename__ = 'user'

    #建立字段函数
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    mobile = db.Column(db.String(200))
    password = db.Column(db.String(200))
    otp = db.Column(db.String(200))   # 随机6位数字的验证码
    created_at = db.Column(db.String(200))


"""
请按要求完成以下api 功能
 Token Api: 通过手机号验证用户(不需要实现发短信功能)
Method: POST
Resource: /token
Payload: {“mobile”: “+86-12388888888”, “otp”: “123456”}
Response: {“access_token”: “xxx”, “refresh_token”: “xxx”, “expiry”: 12345}
 Profile Api: 获取用户本人基本信息
Method: GET
Resource: /profile
Authorization: Bearer token
Response: {“id”: 123, “first_name”: “tom”, “last_name”: “Jerry”}
技术要求：
1) 基于python, flask, Postgresql/MySql，如需要其他请自行决定
2) 通过docker-compose 运行
3) 代码上传到github/gitlab, 完成后请提供git url
4) 请在一周内完成以上功能
"""

@app.route('/test/api/v1.0/token', methods=['POST'])
def create_token():
    if not request.json or not 'mobile' in request.json:
        abort(400)
    obj = request.get_json(force=True)
    get_mobile = obj.get("mobile")
    otp = obj.get("otp")
    if not obj or not get_mobile or not otp:
        return "参数错误"
    if get_mobile:
        access_token,exp_datetime  = generate_access_token(mobile=get_mobile)
        refresh_token = generate_refresh_token(mobile=get_mobile)
        data = {"access_token": access_token.decode("utf-8"),
                "refresh_token": refresh_token.decode("utf-8"),
                "expiry": exp_datetime
                }
        return jsonify(data)
    else:
        return "用户名或密码错误"




@app.route('/test/api/v1.0/profile', methods=['GET'])
@login_required
def get_profile():
    user_id = request.form.get('id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        profile = {
            "id": user_id,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        return jsonify({'profile': profile}),200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
