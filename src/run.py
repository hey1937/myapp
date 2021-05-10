# -*- coding:utf-8 -*-
from flask import Flask, jsonify
from util import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python_dev_user:2Y6eEnp4bAFXNuVh8Tj7@116.62.205.226:3306/trans_tools?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
db.init_app(app)
"""
4JTR 3CA4 SDSD B4JX4JTR 3CA4 SDSD B4JX
"""


class User(db.Model):
    # 声明表名
    __tablename__ = 'user'

    # 建立字段函数
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    mobile = db.Column(db.String(200))
    password = db.Column(db.String(200))
    otp = db.Column(db.String(200))  # 随机6位数字的验证码
    created_at = db.Column(db.String(200))



@app.route("/test/api/v1.0/token", methods=['POST'])
def create_token():
    if request.json:
        obj = request.get_json(force=True)
        get_mobile = obj.get("mobile")
        otp = obj.get("otp")
        if not obj or not get_mobile or not otp:
            data = {
                "msg": "参数错误",
                "status": "500",
            }
            return jsonify(data)
        if get_mobile:
            access_token, exp_datetime = generate_access_token(mobile=get_mobile)
            refresh_token = generate_refresh_token(mobile=get_mobile)
            data = {"access_token": access_token,
                    "refresh_token": refresh_token,
                    "expiry": exp_datetime
                    }
            return jsonify(data)
        else:
            data = {
                "msg": "参数错误",
                "status": "500",
            }
            return jsonify(data)
    else:
        data = {
            "msg": "参数错误",
            "status": "500",
        }
        return jsonify(data)


@app.route('/test/api/v1.0/profile', methods=['GET'])
@login_required
def get_profile():
    if request.method == 'GET':
        user_id = request.args.get('id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            profile = {
                "id": user_id,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
            return jsonify({'profile': profile})
        else:
            data = {
                "msg": "参数错误",
                "status": "500",
            }
            return jsonify(data)
    data = {
        "msg": "参数错误",
        "status": "500",
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
