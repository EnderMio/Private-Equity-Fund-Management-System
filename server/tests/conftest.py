import pytest
from app import create_app
from app.extensions import db  # 从 extensions 导入 db
from app.models import User, Fund, Stock, Holding

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def clear_tables(app):
    with app.app_context():
        db.session.query(Holding).delete()
        db.session.query(Stock).delete()
        db.session.query(Fund).delete()
        db.session.query(User).delete()
        db.session.commit()
