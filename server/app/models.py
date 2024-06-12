from .extensions import db  # 从 extensions 导入 db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# 多对多关系的关联表
user_fund_association = db.Table('user_fund_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('fund_id', db.Integer, db.ForeignKey('fund.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=0)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    funds = db.relationship('Fund', secondary=user_fund_association, lazy='subquery',
                            backref=db.backref('users', lazy=True))
    managed_funds = db.relationship('Fund', backref='manager', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

class Holding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, db.ForeignKey('fund.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    fund = db.relationship('Fund', backref=db.backref('holdings', lazy=True))
    stock = db.relationship('Stock', backref=db.backref('holdings', lazy=True))

class Fund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    amount = db.Column(db.Float)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(64))
    pe_ratio = db.Column(db.Float)
    pb_ratio = db.Column(db.Float)
    total_market_value = db.Column(db.Float)
    inception_date = db.Column(db.Date)
    expense_ratio = db.Column(db.Float)
    nav = db.Column(db.Float)
    risk_level = db.Column(db.String(64))
    return_rate_1y = db.Column(db.Float)
    return_rate_3y = db.Column(db.Float)
    return_rate_5y = db.Column(db.Float)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    pe_ratio = db.Column(db.Float)
    pb_ratio = db.Column(db.Float)
    total_market_value = db.Column(db.Float)
    sector = db.Column(db.String(64))
    ipo_date = db.Column(db.String(10))  # 修改为字符串类型
    dividend_yield = db.Column(db.Float)
    shares_outstanding = db.Column(db.Integer)
    market_type = db.Column(db.String(64))