from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app.main import bp


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    return redirect(url_for('auth.login')) 