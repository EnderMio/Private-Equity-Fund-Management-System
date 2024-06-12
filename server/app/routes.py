from flask import Blueprint, request, jsonify, g, session
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Fund, Stock, Holding
from . import db
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.before_request
def before_request():
    g.user = current_user
    if current_user.is_authenticated:
        print(f"当前用户: {current_user.username}, 角色: {current_user.role}, 会话ID: {session.get('user_id')}")
    else:
        print("当前用户未认证")

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], role=data.get('role', 'user'))  # 默认角色为 user
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        session['user_id'] = user.id  # 设置会话信息
        print(f"用户 {user.username} 登录成功，会话ID: {session['user_id']}")  # 调试信息
        return jsonify({'message': 'Logged in successfully', 'role': user.role}), 200  # 返回用户身份信息
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)  # 移除会话信息
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/funds', methods=['POST'])
@login_required
def create_fund():
    if g.user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    new_fund = Fund(
        name=data['name'],
        description=data.get('description'),
        amount=data.get('amount'),
        manager=data.get('manager'),
        type=data.get('type'),
        expense_ratio=data.get('expense_ratio'),
        risk_level=data.get('risk_level'),
        inception_date=datetime.now()  # 自动填写创建时间
    )

    # 只在前端传递的字段存在时才进行赋值
    optional_fields = ['pe_ratio', 'pb_ratio', 'total_market_value', 'nav', 'return_rate_1y', 'return_rate_3y', 'return_rate_5y', 'asset_allocation', 'dividend_history']
    for field in optional_fields:
        if data.get(field) is not None:
            setattr(new_fund, field, data.get(field))

    db.session.add(new_fund)
    db.session.commit()
    return jsonify({'message': 'Fund created successfully'}), 201


@bp.route('/funds/<int:fund_id>', methods=['PUT'])
@login_required
def update_fund(fund_id):
    if g.user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    fund = db.session.get(Fund, fund_id)
    if not fund:
        return jsonify({'message': 'Fund not found'}), 404
    data = request.get_json()
    fund.name = data.get('name', fund.name)
    fund.description = data.get('description', fund.description)
    fund.amount = data.get('amount', fund.amount)
    fund.manager = data.get('manager', fund.manager)
    fund.type = data.get('type', fund.type)
    fund.pe_ratio = data.get('pe_ratio', fund.pe_ratio)
    fund.pb_ratio = data.get('pb_ratio', fund.pb_ratio)
    fund.total_market_value = data.get('total_market_value', fund.total_market_value)
    fund.inception_date = data.get('inception_date', fund.inception_date)
    fund.expense_ratio = data.get('expense_ratio', fund.expense_ratio)
    fund.nav = data.get('nav', fund.nav)
    fund.risk_level = data.get('risk_level', fund.risk_level)
    fund.return_rate_1y = data.get('return_rate_1y', fund.return_rate_1y)
    fund.return_rate_3y = data.get('return_rate_3y', fund.return_rate_3y)
    fund.return_rate_5y = data.get('return_rate_5y', fund.return_rate_5y)
    fund.asset_allocation = data.get('asset_allocation', fund.asset_allocation)
    fund.dividend_history = data.get('dividend_history', fund.dividend_history)
    db.session.commit()
    return jsonify({'message': 'Fund updated successfully'}), 200

@bp.route('/funds/<int:fund_id>', methods=['DELETE'])
@login_required
def delete_fund(fund_id):
    if g.user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    fund = db.session.get(Fund, fund_id)
    if not fund:
        return jsonify({'message': 'Fund not found'}), 404
    db.session.delete(fund)
    db.session.commit()
    return jsonify({'message': 'Fund deleted successfully'}), 200

@bp.route('/funds', methods=['GET'])
@login_required
def get_all_funds():
    funds = Fund.query.all()
    funds_list = [
        {
            'id': fund.id,
            'name': fund.name,
            'description': fund.description,
            'amount': fund.amount,
            'manager': {
                'id': fund.manager.id,
                'username': fund.manager.username,
                'role': fund.manager.role
            },
            'type': fund.type,
            'total_holdings_value': fund.total_holdings_value,
            'pe_ratio': fund.pe_ratio,
            'pb_ratio': fund.pb_ratio,
            'total_market_value': fund.total_market_value,
            'inception_date': fund.inception_date.isoformat() if fund.inception_date else None,
            'expense_ratio': fund.expense_ratio,
            'nav': fund.nav,
            'risk_level': fund.risk_level,
            'return_rate_1y': fund.return_rate_1y,
            'return_rate_3y': fund.return_rate_3y,
            'return_rate_5y': fund.return_rate_5y,
        }
        for fund in funds
    ]

    return jsonify(funds_list), 200

@bp.route('/funds/<int:fund_id>', methods=['GET'])
@login_required
def get_fund_details(fund_id):
    fund = db.session.get(Fund, fund_id)
    if not fund:
        return jsonify({'message': 'Fund not found'}), 404

    manager = User.query.get(fund.manager_id)

    return jsonify({
        'id': fund.id,
        'name': fund.name,
        'description': fund.description,
        'amount': fund.amount,
        'manager': {
            'id': manager.id,
            'username': manager.username,
            'role': manager.role
        },
        'type': fund.type,
        'total_holdings_value': fund.total_holdings_value,
        'pe_ratio': fund.pe_ratio,
        'pb_ratio': fund.pb_ratio,
        'total_market_value': fund.total_market_value,
        'inception_date': fund.inception_date.isoformat() if fund.inception_date else None,
        'expense_ratio': fund.expense_ratio,
        'nav': fund.nav,
        'risk_level': fund.risk_level,
        'return_rate_1y': fund.return_rate_1y,
        'return_rate_3y': fund.return_rate_3y,
        'return_rate_5y': fund.return_rate_5y,
        'holdings': [
            {
                'stock_id': holding.stock_id,
                'stock_name': holding.stock.name,
                'quantity': holding.quantity
            }
            for holding in fund.holdings
        ]
    }), 200
    
@bp.route('/funds/manager/<string:username>', methods=['GET'])
@login_required
def get_funds_by_manager(username):
    if current_user.role != 'admin' and current_user.role != 'manager':
        return jsonify({'message': 'Unauthorized'}), 403

    manager = User.query.filter_by(username=username, role='manager').first()
    if not manager:
        return jsonify({'message': 'Manager not found'}), 404

    funds = Fund.query.filter_by(manager_id=manager.id).all()
    funds_list = [
        {
            'id': fund.id,
            'name': fund.name,
            'description': fund.description,
            'amount': fund.amount,
            'manager': {
                'id': manager.id,
                'username': manager.username,
                'role': manager.role
            },
            'type': fund.type,
            'total_holdings_value': fund.total_holdings_value,
            'pe_ratio': fund.pe_ratio,
            'pb_ratio': fund.pb_ratio,
            'total_market_value': fund.total_market_value,
            'inception_date': fund.inception_date.isoformat() if fund.inception_date else None,
            'expense_ratio': fund.expense_ratio,
            'nav': fund.nav,
            'risk_level': fund.risk_level,
            'return_rate_1y': fund.return_rate_1y,
            'return_rate_3y': fund.return_rate_3y,
            'return_rate_5y': fund.return_rate_5y,
        }
        for fund in funds
    ]

    return jsonify(funds_list), 200

@bp.route('/stocks', methods=['POST'])
@login_required
def add_stock():
    if g.user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    new_stock = Stock(
        symbol=data['symbol'],
        name=data['name'],
        price=data['price'],
        pe_ratio=data.get('pe_ratio'),
        pb_ratio=data.get('pb_ratio'),
        total_market_value=data.get('total_market_value'),
        sector=data.get('sector'),
        ipo_date=data.get('ipo_date'),  # 使用字符串类型
        dividend_yield=data.get('dividend_yield'),
        shares_outstanding=data.get('shares_outstanding'),
        market_type=data.get('market_type')
    )
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({'message': 'Stock added successfully'}), 201

@bp.route('/stocks/<int:stock_id>', methods=['PUT'])
@login_required
def update_stock(stock_id):
    if g.user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    stock = db.session.get(Stock, stock_id)
    if not stock:
        return jsonify({'message': 'Stock not found'}), 404
    data = request.get_json()
    stock.symbol = data.get('symbol', stock.symbol)
    stock.name = data.get('name', stock.name)
    stock.price = data.get('price', stock.price)
    stock.pe_ratio = data.get('pe_ratio', stock.pe_ratio)
    stock.pb_ratio = data.get('pb_ratio', stock.pb_ratio)
    stock.total_market_value = data.get('total_market_value', stock.total_market_value)
    stock.sector = data.get('sector', stock.sector)
    stock.dividend_yield = data.get('dividend_yield', stock.dividend_yield)
    stock.shares_outstanding = data.get('shares_outstanding', stock.shares_outstanding)
    stock.market_type = data.get('market_type', stock.market_type)
    stock.ipo_date = data.get('ipo_date', stock.ipo_date)  # 使用字符串类型

    db.session.commit()
    return jsonify({
        'message': 'Stock updated successfully',
        'stock': {
            'id': stock.id,
            'symbol': stock.symbol,
            'name': stock.name,
            'price': stock.price,
            'pe_ratio': stock.pe_ratio,
            'pb_ratio': stock.pb_ratio,
            'total_market_value': stock.total_market_value,
            'sector': stock.sector,
            'ipo_date': stock.ipo_date,  # 使用字符串类型
            'dividend_yield': stock.dividend_yield,
            'shares_outstanding': stock.shares_outstanding,
            'market_type': stock.market_type
        }
    }), 200

@bp.route('/stocks/<int:stock_id>', methods=['DELETE'])
@login_required
def delete_stock(stock_id):
    if g.user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    stock = db.session.get(Stock, stock_id)
    if not stock:
        return jsonify({'message': 'Stock not found'}), 404
    db.session.delete(stock)
    db.session.commit()
    return jsonify({'message': 'Stock deleted successfully'}), 200

@bp.route('/stocks', methods=['GET'])
@login_required
def get_stocks():
    stocks = Stock.query.all()
    stocks_list = [
        {
            'id': stock.id,
            'symbol': stock.symbol,
            'name': stock.name,
            'price': stock.price,
            'pe_ratio': stock.pe_ratio,
            'pb_ratio': stock.pb_ratio,
            'total_market_value': stock.total_market_value,
            'sector': stock.sector,
            'ipo_date': stock.ipo_date,  # 使用字符串类型
            'dividend_yield': stock.dividend_yield,
            'shares_outstanding': stock.shares_outstanding,
            'market_type': stock.market_type
        }
        for stock in stocks
    ]
    return jsonify(stocks_list), 200

@bp.route('/funds/<int:fund_id>/holdings', methods=['POST'])
@login_required
def add_holding(fund_id):
    if g.user.role != 'manager':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    new_holding = Holding(fund_id=fund_id, stock_id=data['stock_id'], quantity=data['quantity'])
    db.session.add(new_holding)
    db.session.commit()
    return jsonify({'message': 'Holding added successfully'}), 201

@bp.route('/funds/<int:fund_id>/holdings/<int:holding_id>', methods=['PUT'])
@login_required
def update_holding(fund_id, holding_id):
    if g.user.role != 'manager':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    holding = Holding.query.get_or_404(holding_id)
    if holding.fund_id != fund_id:
        return jsonify({'message': 'Invalid fund ID'}), 400
    holding.stock_id = data.get('stock_id', holding.stock_id)
    holding.quantity = data.get('quantity', holding.quantity)
    db.session.commit()
    return jsonify({'message': 'Holding updated successfully'}), 200

@bp.route('/funds/<int:fund_id>/holdings', methods=['GET'])
@login_required
def get_holdings(fund_id):
    holdings = Holding.query.filter_by(fund_id=fund_id).all()
    holdings_list = [{'stock_id': holding.stock_id, 'stock_name': holding.stock.name, 'quantity': holding.quantity} for holding in holdings]
    return jsonify(holdings_list), 200

@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    role = request.args.get('role')
    
    # 检查角色参数是否有效
    if role not in ['admin', 'manager', 'user']:
        return jsonify({'message': 'Invalid role'}), 400

    # 权限控制逻辑
    if current_user.role != 'admin':
        if role == 'admin' or role == 'user':
            return jsonify({'message': 'Unauthorized'}), 403
        elif role == 'manager':
            users = User.query.filter_by(role='manager').all()
    else:
        users = User.query.filter_by(role=role).all()
    
    users_list = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
    
    return jsonify(users_list), 200

@bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # 检查是否是管理员或用户本人
    if g.user.role != 'admin' and g.user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.set_password(data['password'])
    if 'role' in data and g.user.role == 'admin':  # 只有管理员可以更改角色
        user.role = data['role']
    
    db.session.commit()
    
    return jsonify({'message': 'User updated successfully'}), 200

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if g.user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200

@bp.route('/user/<username>/funds', methods=['GET'])
@login_required
def get_user_funds(username):
    user = User.query.filter_by(username=username, role='user').first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    funds = user.funds
    funds_list = [
        {
            'id': fund.id,
            'name': fund.name,
            'description': fund.description,
            'amount': fund.amount,
            'manager': fund.manager.username,
            'type': fund.type,
            'pe_ratio': fund.pe_ratio,
            'pb_ratio': fund.pb_ratio,
            'total_market_value': fund.total_market_value,
            'inception_date': fund.inception_date.isoformat() if fund.inception_date else None,
            'expense_ratio': fund.expense_ratio,
            'nav': fund.nav,
            'risk_level': fund.risk_level,
            'return_rate_1y': fund.return_rate_1y,
            'return_rate_3y': fund.return_rate_3y,
            'return_rate_5y': fund.return_rate_5y,
            'total_holdings_value': fund.total_holdings_value
        }
        for fund in funds
    ]
    return jsonify(funds_list), 200