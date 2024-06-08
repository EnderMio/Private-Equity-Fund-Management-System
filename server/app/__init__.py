from flask import Flask
from flask_cors import CORS
from .extensions import db, login_manager
from .models import User
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化数据库和登录管理器
    db.init_app(app)
    login_manager.init_app(app)

    # 允许跨域请求
    CORS(app, supports_credentials=True)

    # 创建所有数据库表，并确保存在管理员用户
    with app.app_context():
        db.create_all()
        ensure_admin_exists()

    # 注册蓝图
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # 设置日志记录
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask startup')

    return app

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def ensure_admin_exists():
    admin_username = 'admin'
    admin_password = 'admin_password'  # 设置默认管理员密码
    admin = User.query.filter_by(username=admin_username).first()
    if not admin:
        admin = User(username=admin_username, role='admin')
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
