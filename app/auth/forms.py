from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError, EqualTo
from app.models import User

"""
一个表单
由于Flask-WTF插件本身不提供字段类型，
因此我直接从WTForms包中导入了四个表示表单字段的类。
每个字段类都接受一个描述或别名作为第一个参数，
并生成一个实例来作为LoginForm的类属性
你在一些字段中看到的可选参数validators用于验证输入字段是否符合预期。
DataRequired验证器仅验证字段输入是否为空。
更多的验证器将会在未来的表单中接触到
"""


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), ])
    # email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


"""

"""


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already registered.')
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')


class EditUserForm(FlaskForm):

    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])

    submit = SubmitField('Update')
    def validate_current_password(self, current_password):
        user = User.query.filter_by(id=current_user.id).first()
        if not user.check_password(current_password.data):
            raise ValidationError('Current password is incorrect.')

class PostForm(FlaskForm):
    body = TextAreaField('Enter something', validators=[DataRequired()])
    submit = SubmitField('Submit')

