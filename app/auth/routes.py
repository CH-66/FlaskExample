from datetime import datetime, UTC
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.auth.forms import LoginForm,RegistrationForm
from app.models import User,db
from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route("/index", methods=["GET"])
@login_required
def index():
    post={
        'author': {'username': 'zy'},
        'body': 'Beautiful day in Portland!'
    }
    return render_template('index.html', title='Home', post=post)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.index')
        # 如果登录URL中包含next参数，其值是一个包含域名的完整URL，那么重定向到本应用的主页。
        return redirect(next_page)
    flash('Invalid username or password')
    return render_template("login.html", title='Sign In', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

