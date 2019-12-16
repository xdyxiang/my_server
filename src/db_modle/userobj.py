# coding=utf8

from src.app import app, db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature



class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    remark = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 建立user表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    status = db.Column(db.String(100))
    userinfo = db.relationship('UserInfo', backref='user')



    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=7200):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            msg = 'valid token, but expired'
            return False,msg  # valid token, but expired
        except BadSignature:
            msg = 'Invalid token'
            return False,msg  # invalid token
        user = User.query.get(data['id'])# 根据主键查询
        return True,user
