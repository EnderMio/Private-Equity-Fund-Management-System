import pytest
from app import create_app, db
from app.models import User, Fund, Stock, Holding
from flask import session

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        user = User(username='testuser', role='user')
        user.set_password('password')
        admin = User(username='adminuser', role='admin')
        admin.set_password('password')
        db.session.add(user)
        db.session.add(admin)
        fund = Fund(name='Test Fund', description='A test fund')
        stock = Stock(symbol='TEST', name='Test Stock')
        db.session.add(fund)
        db.session.add(stock)
        db.session.commit()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()

def login(client, username, password):
    return client.post('/login', json={'username': username, 'password': password})

def test_register(client):
    response = client.post('/register', json={'username': 'newuser', 'password': 'password'})
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_login(client):
    response = login(client, 'testuser', 'password')
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

def test_create_fund(client):
    login(client, 'adminuser', 'password')
    response = client.post('/funds', json={'name': 'Another Test Fund', 'description': 'Another test fund'})
    assert response.status_code == 201
    assert b'Fund created successfully' in response.data

def test_create_fund_user(client):
    login(client, 'testuser', 'password')
    response = client.post('/funds', json={'name': 'User Test Fund', 'description': 'User test fund'})
    assert response.status_code == 403
    assert b'Unauthorized' in response.data

def test_update_fund(client):
    login(client, 'adminuser', 'password')
    response = client.put('/funds/1', json={'name': 'Updated Test Fund'})
    assert response.status_code == 200
    assert b'Fund updated successfully' in response.data

def test_update_fund_user(client):
    login(client, 'testuser', 'password')
    response = client.put('/funds/1', json={'name': 'Updated User Test Fund'})
    assert response.status_code == 403
    assert b'Unauthorized' in response.data

def test_delete_fund(client):
    login(client, 'adminuser', 'password')
    response = client.delete('/funds/1')
    assert response.status_code == 200
    assert b'Fund deleted successfully' in response.data

def test_delete_fund_user(client):
    login(client, 'testuser', 'password')
    response = client.delete('/funds/1')
    assert response.status_code == 403
    assert b'Unauthorized' in response.data

def test_add_stock(client):
    login(client, 'adminuser', 'password')
    response = client.post('/stocks', json={'symbol': 'NEW', 'name': 'New Stock'})
    assert response.status_code == 201
    assert b'Stock added successfully' in response.data

def test_add_stock_user(client):
    login(client, 'testuser', 'password')
    response = client.post('/stocks', json={'symbol': 'NEWUSER', 'name': 'New User Stock'})
    assert response.status_code == 403
    assert b'Unauthorized' in response.data

def test_update_stock(client):
    login(client, 'adminuser', 'password')
    response = client.put('/stocks/1', json={'symbol': 'TEST', 'name': 'Updated Test Stock'})
    assert response.status_code == 200
    assert b'Stock updated successfully' in response.data

def test_update_stock_user(client):
    login(client, 'testuser', 'password')
    response = client.put('/stocks/1', json={'symbol': 'USERTEST', 'name': 'Updated User Test Stock'})
    assert response.status_code == 403
    assert b'Unauthorized' in response.data

def test_delete_stock(client):
    login(client, 'adminuser', 'password')
    response = client.delete('/stocks/1')
    assert response.status_code == 200
    assert b'Stock deleted successfully' in response.data

def test_delete_stock_user(client):
    login(client, 'testuser', 'password')
    response = client.delete('/stocks/1')
    assert response.status_code == 403
    assert b'Unauthorized' in response.data

def test_add_holding(client):
    login(client, 'adminuser', 'password')
    response = client.post('/funds', json={'name': 'Holding Fund', 'description': 'A holding fund'})
    assert response.status_code == 201
    assert b'Fund created successfully' in response.data
    response = client.post('/stocks', json={'symbol': 'HOLD', 'name': 'Holding Stock'})
    assert response.status_code == 201
    assert b'Stock added successfully' in response.data
    response = client.post('/funds/2/holdings', json={'stock_id': 2, 'quantity': 100})
    assert response.status_code == 201
    assert b'Holding added successfully' in response.data

def test_add_holding_user(client):
    login(client, 'testuser', 'password')
    response = client.post('/funds/1/holdings', json={'stock_id': 1, 'quantity': 50})
    assert response.status_code == 403
    assert b'Unauthorized' in response.data
