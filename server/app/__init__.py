from flask import Flask
from flask_cors import CORS
from .extensions import db, login_manager
from .models import User, Fund, Stock, Holding, user_fund_association
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化数据库和登录管理器
    db.init_app(app)
    login_manager.init_app(app)

    # 允许跨域请求
    CORS(app, supports_credentials=True)

    # 创建所有数据库表，并确保存在管理员用户和样例数据
    with app.app_context():
        db.create_all()
        ensure_admin_exists()
        add_sample_data()

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

from datetime import datetime

from datetime import datetime

def add_sample_data():
    if not User.query.filter_by(role='manager').first():
        # 添加样例基金经理用户
        manager1 = User(username='manager1', role='manager')
        manager1.set_password('password1')
        manager2 = User(username='manager2', role='manager')
        manager2.set_password('password2')
        ender_mio = User(username='EnderMio', role='manager')
        ender_mio.set_password('123456')
        db.session.add_all([manager1, manager2, ender_mio])
        db.session.commit()

    if not User.query.filter_by(role='user').first():
        # 添加样例普通用户
        user1 = User(username='user1', role='user')
        user1.set_password('password1')
        user2 = User(username='user2', role='user')
        user2.set_password('password2')
        db.session.add_all([user1, user2])
        db.session.commit()

    if not Fund.query.first():
        # 添加样例基金数据
        manager1 = User.query.filter_by(username='manager1').first()
        manager2 = User.query.filter_by(username='manager2').first()
        ender_mio = User.query.filter_by(username='EnderMio').first()

        fund1 = Fund(
            name='样例基金1',
            description='这是一个测试用的样例基金',
            amount=1000000.0,
            manager=manager1,
            type='股票型',
            pe_ratio=15.0,
            pb_ratio=1.5,
            total_market_value=1000000.0,
            inception_date=datetime.strptime('2022-01-01', '%Y-%m-%d').date(),
            expense_ratio=0.01,
            nav=10.0,
            risk_level='中等',
            return_rate_1y=0.1,
            return_rate_3y=0.3,
            return_rate_5y=0.5
        )
        fund2 = Fund(
            name='样例基金2',
            description='这是另一个测试用的样例基金',
            amount=2000000.0,
            manager=manager2,
            type='债券型',
            pe_ratio=12.0,
            pb_ratio=1.2,
            total_market_value=2000000.0,
            inception_date=datetime.strptime('2021-01-01', '%Y-%m-%d').date(),
            expense_ratio=0.02,
            nav=20.0,
            risk_level='低',
            return_rate_1y=0.05,
            return_rate_3y=0.15,
            return_rate_5y=0.25
        )
        ender_fund = Fund(
            name='EnderMio基金',
            description='由EnderMio管理的测试基金',
            amount=3000000.0,
            manager=ender_mio,
            type='混合型',
            pe_ratio=18.0,
            pb_ratio=1.8,
            total_market_value=3000000.0,
            inception_date=datetime.strptime('2020-01-01', '%Y-%m-%d').date(),
            expense_ratio=0.02,
            nav=15.0,
            risk_level='中高',
            return_rate_1y=0.12,
            return_rate_3y=0.25,
            return_rate_5y=0.35
        )
        db.session.add_all([fund1, fund2, ender_fund])
        db.session.commit()

    if not Stock.query.first():
        # 添加样例股票数据
        stock1 = Stock(
            symbol='AAPL',
            name='苹果公司',
            price=150.0,
            pe_ratio=30.0,
            pb_ratio=10.0,
            total_market_value=2000000000.0,
            sector='科技',
            ipo_date='1980-12-12',
            dividend_yield=0.015,
            shares_outstanding=500000000,
            market_type='NASDAQ'
        )
        stock2 = Stock(
            symbol='MSFT',
            name='微软公司',
            price=250.0,
            pe_ratio=35.0,
            pb_ratio=12.0,
            total_market_value=1800000000.0,
            sector='科技',
            ipo_date='1986-03-13',
            dividend_yield=0.02,
            shares_outstanding=750000000,
            market_type='NASDAQ'
        )
        stock3 = Stock(
            symbol='GOOGL',
            name='谷歌公司',
            price=2700.0,
            pe_ratio=25.0,
            pb_ratio=5.0,
            total_market_value=1800000000000.0,
            sector='科技',
            ipo_date='2004-08-19',
            dividend_yield=0.0,
            shares_outstanding=300000000,
            market_type='NASDAQ'
        )
        stock4 = Stock(
            symbol='AMZN',
            name='亚马逊公司',
            price=3300.0,
            pe_ratio=60.0,
            pb_ratio=20.0,
            total_market_value=1600000000000.0,
            sector='科技',
            ipo_date='1997-05-15',
            dividend_yield=0.0,
            shares_outstanding=500000000,
            market_type='NASDAQ'
        )
        stock5 = Stock(
            symbol='TSLA',
            name='特斯拉公司',
            price=700.0,
            pe_ratio=300.0,
            pb_ratio=30.0,
            total_market_value=700000000000.0,
            sector='汽车',
            ipo_date='2010-06-29',
            dividend_yield=0.0,
            shares_outstanding=1000000000,
            market_type='NASDAQ'
        )
        db.session.add_all([stock1, stock2, stock3, stock4, stock5])
        db.session.commit()

    if not Holding.query.first():
        # 添加样例持仓数据
        fund1 = Fund.query.filter_by(name='样例基金1').first()
        fund2 = Fund.query.filter_by(name='样例基金2').first()
        ender_fund = Fund.query.filter_by(name='EnderMio基金').first()
        stock1 = Stock.query.filter_by(symbol='AAPL').first()
        stock2 = Stock.query.filter_by(symbol='MSFT').first()
        stock3 = Stock.query.filter_by(symbol='GOOGL').first()
        stock4 = Stock.query.filter_by(symbol='AMZN').first()
        stock5 = Stock.query.filter_by(symbol='TSLA').first()
        holding1 = Holding(
            fund_id=fund1.id,
            stock_id=stock1.id,
            quantity=1000
        )
        holding2 = Holding(
            fund_id=fund2.id,
            stock_id=stock2.id,
            quantity=2000
        )
        holding3 = Holding(
            fund_id=ender_fund.id,
            stock_id=stock1.id,
            quantity=1500
        )
        holding4 = Holding(
            fund_id=ender_fund.id,
            stock_id=stock3.id,
            quantity=500
        )
        holding5 = Holding(
            fund_id=ender_fund.id,
            stock_id=stock4.id,
            quantity=300
        )
        holding6 = Holding(
            fund_id=ender_fund.id,
            stock_id=stock5.id,
            quantity=700
        )
        db.session.add_all([holding1, holding2, holding3, holding4, holding5, holding6])
        db.session.commit()

    # 添加用户持有基金数据
    if not db.session.query(user_fund_association).first():
        user1 = User.query.filter_by(username='user1').first()
        user2 = User.query.filter_by(username='user2').first()
        fund1 = Fund.query.filter_by(name='样例基金1').first()
        fund2 = Fund.query.filter_by(name='样例基金2').first()
        
        # 插入数据到关联表时提供 quantity 字段
        db.session.execute(user_fund_association.insert().values(user_id=user1.id, fund_id=fund1.id, quantity=100))
        db.session.execute(user_fund_association.insert().values(user_id=user2.id, fund_id=fund2.id, quantity=200))
        
        db.session.commit()