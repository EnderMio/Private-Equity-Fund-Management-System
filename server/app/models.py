from .extensions import db  # 从 extensions 导入 db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
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
    manager = db.Column(db.String(64))
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
