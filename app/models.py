from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
db = SQLAlchemy()
# from app import login
"""
Flask-SQLAlchemy提供了两种方式来定义模型。
第一种是使用类来定义模型，第二种是使用db.Model的子类来定义模型。
"""
"""
Flask-Login提供了一个叫做UserMixin的mixin类来将它们归纳其中。
"""
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    about_me = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    def set_password(self, password):
        """
        对用户输入的密码进行哈希处理并存储
        :param password: 用户输入的明文密码
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        验证用户输入的密码是否正确
        :param password: 用户输入的明文密码
        :return: 如果密码正确返回 True，否则返回 False
        """
        return check_password_hash(self.password_hash, password)
    def avatar(self, size):
        """
        生成用户头像的URL
        :param size: 头像大小
        :return: 头像URL
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    def follow(self, user):
        """
        关注用户
        :param user: 要关注的用户
        """
        if not self.is_following(user):
            self.followed.append(user)
    def unfollow(self, user):
        """
        取消关注用户
        :param user: 要取消关注的用户
        """
        if self.is_following(user):
            self.followed.remove(user)
    def is_following(self, user):
        """
        判断是否关注了用户
        :param user: 要判断的用户
        :return: 如果关注了返回 True，否则返回 False
        """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def __repr__(self):
        return '<User %r>' % self.username
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(64), unique=True)
    # slug = db.Column(db.String(64), unique=True)
    body = db.Column(db.Text)
    # body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Post {}>'.format(self.body)

