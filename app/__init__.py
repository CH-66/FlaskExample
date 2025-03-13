import logging
import os
from datetime import datetime, UTC
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from app.auth import init_app as init_auth
from app.errors import init_app as init_errors
from app.main import init_app as init_main
from app.models import db
from config import config




def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    
    # 初始化登录管理器
    login = LoginManager()
    login.login_view = 'auth.login'
    login.init_app(app)
    # 初始化Bootstrap
    bootstrap = Bootstrap(app)

    # 注册蓝图
    init_auth(app)
    init_errors(app)

    # 注册主蓝图
    init_main(app)

    # 初始化数据库迁移
    migrate = Migrate(app, db)
    
    # 添加用户加载函数
    # 在每次请求时，Flask-Login 都需要知道当前用户是谁。
    # 为此，它会自动调用通过 @login.user_loader 装饰器注册的用户加载函数。
    from app.models import User
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # ####可选方案 - 配置日志文件

    # if not app.debug and not app.testing:
    #     # 配置日志文件
    #     if not os.path.exists('logs'):
    #         os.mkdir('logs')
    #     file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    #     file_handler.setFormatter(logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    #     ))
    #     file_handler.setLevel(logging.INFO)
    #     app.logger.addHandler(file_handler)
    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('App startup')

    # ####可选方案 - 缓存支持

    # from flask_caching import Cache
    #
    # cache = Cache()
    # cache.init_app(app, config={'CACHE_TYPE': 'simple'})

    # ####可选方案 -  CSRF 保护
    # 虽然 Flask-WTF 提供了 CSRF 保护，但如果你使用的是纯 Flask-Form 或其他表单处理方式，建议显式启用 CSRF 保护

    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect()
    csrf.init_app(app)

    # ####可选方案 -  任务队列支持
    # from flask_rq2 import RQ
    # rq = RQ()
    # rq.init_app(app)
    #
    # ####可选方案 -  邮件支持
    # from flask_mail import Mail
    # mail = Mail()
    # mail.init_app(app)


    #  请求上下文钩子
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.now(UTC)
            db.session.commit()



    return app

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# # app.register_blueprint(auth_bp, url_prefix='/auth')
# migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'
# bootstrap = Bootstrap(app)


