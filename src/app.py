from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from response.common_response import ResponseResult

app = Flask(__name__)

# 配置 SQLite 数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# 关闭追踪修改（节省开销）
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 通过flask实例，创建 SQLAlchemy 实例
db = SQLAlchemy(app)


# 定义 UserInfo 模型（对应 user_info 表）
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 用户姓名
    user_name = db.Column(db.String(10), nullable=False)
    # 用户昵称（支付宝/微信）
    nick_name = db.Column(db.String(30), nullable=False)
    # 和手机号通过微信获取
    phone_number = db.Column(db.String(20), nullable=False)
    # 保险公司名称
    company_name = db.Column(db.String(30), nullable=False)
    # 保险公司电话
    company_phone = db.Column(db.String(20), nullable=False)
    # 保险补充信息截图（外链）
    img_ext = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'nick_name': self.nick_name,
            'phone_number': self.phone_number,
            'company_name': self.company_name,
            'company_phone': self.company_phone,
            'img_ext': self.img_ext
        }


# 创建表，在应用启动时调用函数
@app.before_request
def create_tables():
    db.create_all()


# 插入一条用户记录
@app.route('/v1/add_user', methods=['POST'])
def add_user():
    req_body = request.json
    insert_user = UserInfo(
        user_name=req_body.get('user_name', ''),  # 如果不存在，赋空字符串
        nick_name=req_body.get('nick_name', ''),
        phone_number=req_body.get('phone_number', ''),
        company_name=req_body.get('company_name', ''),
        company_phone=req_body.get('company_phone', ''),
        img_ext=req_body.get('img_ext', ''),
    )
    db.session.add(insert_user)
    db.session.commit()
    return jsonify(ResponseResult().to_dict())


# 查询所有用户
@app.route('/all/users')
def get_all_users():
    user_infos = UserInfo.query.all()
    user_list = [
        {'id': user.id,
         'user_name': user.user_name,
         'nick_name': user.nick_name,
         'phone_number': user.phone_number,
         'company_name': user.company_name,
         'company_phone': user.company_phone,
         'img_ext': user.img_ext
         } for user in user_infos]
    return jsonify(ResponseResult(data=user_list).to_dict())

# 根据用户名和手机号查询用户投保信息
@app.route('/search')
def search_users():
    user_name = request.args.get('user_name')
    phone_number = request.args.get('phone_number')
    if not user_name or not phone_number:
        pass
    filtered_users = UserInfo.query.filter_by(user_name=user_name, phone_number=phone_number).all()
    user_list = [user.to_dict() for user in filtered_users]
    return jsonify(ResponseResult(data=user_list).to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
