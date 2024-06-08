import pytest
from app import create_app, db
from app.models import User, Fund, Stock, Holding

@pytest.fixture
def app_context():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_user_model(app_context):
    with app_context.app_context():
        user = User(username="testuser", role="user")
        user.set_password("password")
        assert user.username == "testuser"
        assert user.check_password("password")

def test_fund_model(app_context):
    with app_context.app_context():
        fund = Fund(name="testfund", description="A test fund")
        db.session.add(fund)
        db.session.commit()
        assert fund.name == "testfund"
        assert fund.description == "A test fund"

def test_stock_model(app_context):
    with app_context.app_context():
        stock = Stock(symbol="TST", name="Test Stock")
        db.session.add(stock)
        db.session.commit()
        assert stock.symbol == "TST"
        assert stock.name == "Test Stock"

def test_holding_model(app_context):
    with app_context.app_context():
        fund = Fund(name="testfund", description="A test fund")
        stock = Stock(symbol="TST", name="Test Stock")
        db.session.add(fund)
        db.session.add(stock)
        db.session.commit()

        holding = Holding(fund_id=fund.id, stock_id=stock.id, quantity=10)
        db.session.add(holding)
        db.session.commit()
        assert holding.fund_id == fund.id
        assert holding.stock_id == stock.id
        assert holding.quantity == 10
