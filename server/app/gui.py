from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QSpacerItem, QSizePolicy, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt
import requests
import sys

BASE_URL = "http://127.0.0.1:5000"  # 后端API的基础URL

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My PyQt App")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        self.clear_layout()

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.label = QLabel("Welcome to the PyQt App", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        self.choice_label = QLabel("Choose an option:", self)
        self.choice_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.choice_label)
        
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.switch_to_login)
        self.layout.addWidget(self.login_button)
        
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.switch_to_register)
        self.layout.addWidget(self.register_button)
        
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)
        
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def clear_layout(self):
        if self.layout is not None:
            while self.layout.count():
                item = self.layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def switch_to_login(self):
        self.clear_layout()

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.layout.addWidget(QLabel("Username"))
        self.username_entry = QLineEdit(self)
        self.layout.addWidget(self.username_entry)
        
        self.layout.addWidget(QLabel("Password"))
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_entry)
        
        self.login_submit_button = QPushButton("Login", self)
        self.login_submit_button.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_submit_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.initUI)
        self.layout.addWidget(self.back_button)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


    def switch_to_register(self):
        self.clear_layout()

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.layout.addWidget(QLabel("Username"))
        self.username_entry = QLineEdit(self)
        self.layout.addWidget(self.username_entry)
        
        self.layout.addWidget(QLabel("Password"))
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_entry)
        
        self.register_submit_button = QPushButton("Register", self)
        self.register_submit_button.clicked.connect(self.handle_register)
        self.layout.addWidget(self.register_submit_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.initUI)
        self.layout.addWidget(self.back_button)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def handle_login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        payload = {
            "username": username,
            "password": password
        }

        try:
            print(f"Sending POST request to {BASE_URL}/login with payload: {payload}")
            response = requests.post(f"{BASE_URL}/login", json=payload)
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Login successful!")
                self.switch_to_dashboard(username)
            else:
                QMessageBox.critical(self, "Error", f"Failed to login: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to login: {e}")


    def handle_register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        payload = {
            "username": username,
            "password": password
        }

        try:
            print(f"Sending POST request to {BASE_URL}/register with payload: {payload}")
            response = requests.post(f"{BASE_URL}/register", json=payload)
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 201:
                QMessageBox.information(self, "Success", "User registered successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to register user: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to register user: {e}")


    def switch_to_dashboard(self, username):
        self.clear_layout()

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        welcome_label = QLabel(f"Welcome, {username}!", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(welcome_label)

        fund_mgmt_button = QPushButton("Fund Management", self)
        fund_mgmt_button.clicked.connect(self.switch_to_fund_management)
        self.layout.addWidget(fund_mgmt_button)

        stock_mgmt_button = QPushButton("Stock Management", self)
        stock_mgmt_button.clicked.connect(self.switch_to_stock_management)
        self.layout.addWidget(stock_mgmt_button)

        user_mgmt_button = QPushButton("User Management", self)
        user_mgmt_button.clicked.connect(self.switch_to_user_management)
        self.layout.addWidget(user_mgmt_button)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.initUI)
        self.layout.addWidget(self.logout_button)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


    def switch_to_fund_management(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Fund Management", self))

        self.create_fund_button = QPushButton("Create Fund", self)
        self.create_fund_button.clicked.connect(self.create_fund)
        self.layout.addWidget(self.create_fund_button)

        self.update_fund_button = QPushButton("Update Fund", self)
        self.update_fund_button.clicked.connect(self.update_fund)
        self.layout.addWidget(self.update_fund_button)

        self.delete_fund_button = QPushButton("Delete Fund", self)
        self.delete_fund_button.clicked.connect(self.delete_fund)
        self.layout.addWidget(self.delete_fund_button)

        self.view_fund_button = QPushButton("View Fund Details", self)
        self.view_fund_button.clicked.connect(self.view_fund)
        self.layout.addWidget(self.view_fund_button)

        self.back_button = QPushButton("Back to Dashboard", self)
        self.back_button.clicked.connect(self.switch_to_dashboard)
        self.layout.addWidget(self.back_button)

    def create_fund(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Create Fund", self))

        self.layout.addWidget(QLabel("Fund Name"))
        self.fund_name_entry = QLineEdit(self)
        self.layout.addWidget(self.fund_name_entry)
        
        self.layout.addWidget(QLabel("Fund Amount"))
        self.fund_amount_entry = QLineEdit(self)
        self.layout.addWidget(self.fund_amount_entry)

        self.create_fund_submit_button = QPushButton("Create Fund", self)
        self.create_fund_submit_button.clicked.connect(self.handle_create_fund)
        self.layout.addWidget(self.create_fund_submit_button)

        self.back_button = QPushButton("Back to Fund Management", self)
        self.back_button.clicked.connect(self.switch_to_fund_management)
        self.layout.addWidget(self.back_button)

    def handle_create_fund(self):
        fund_name = self.fund_name_entry.text()
        fund_amount = self.fund_amount_entry.text()

        payload = {
            "name": fund_name,
            "amount": fund_amount
        }

        try:
            print(f"Sending POST request to {BASE_URL}/funds with payload: {payload}")
            response = requests.post(f"{BASE_URL}/funds", json=payload)
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Fund created successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to create fund: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create fund: {e}")

    def update_fund(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Update Fund", self))

        self.layout.addWidget(QLabel("Fund ID"))
        self.fund_id_entry = QLineEdit(self)
        self.layout.addWidget(self.fund_id_entry)

        self.layout.addWidget(QLabel("New Fund Name"))
        self.fund_name_entry = QLineEdit(self)
        self.layout.addWidget(self.fund_name_entry)
        
        self.layout.addWidget(QLabel("New Fund Amount"))
        self.fund_amount_entry = QLineEdit(self)
        self.layout.addWidget(self.fund_amount_entry)

        self.update_fund_submit_button = QPushButton("Update Fund", self)
        self.update_fund_submit_button.clicked.connect(self.handle_update_fund)
        self.layout.addWidget(self.update_fund_submit_button)

        self.back_button = QPushButton("Back to Fund Management", self)
        self.back_button.clicked.connect(self.switch_to_fund_management)
        self.layout.addWidget(self.back_button)

    def handle_update_fund(self):
        fund_id = self.fund_id_entry.text()
        fund_name = self.fund_name_entry.text()
        fund_amount = self.fund_amount_entry.text()

        payload = {
            "name": fund_name,
            "amount": fund_amount
        }

        try:
            print(f"Sending PUT request to {BASE_URL}/funds/{fund_id} with payload: {payload}")
            response = requests.put(f"{BASE_URL}/funds/{fund_id}", json=payload)
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Fund updated successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to update fund: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update fund: {e}")

    def delete_fund(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Delete Fund", self))

        self.layout.addWidget(QLabel("Fund ID"))
        self.fund_id_entry = QLineEdit(self)
        self.layout.addWidget(self.fund_id_entry)

        self.delete_fund_submit_button = QPushButton("Delete Fund", self)
        self.delete_fund_submit_button.clicked.connect(self.handle_delete_fund)
        self.layout.addWidget(self.delete_fund_submit_button)

        self.back_button = QPushButton("Back to Fund Management", self)
        self.back_button.clicked.connect(self.switch_to_fund_management)
        self.layout.addWidget(self.back_button)

    def handle_delete_fund(self):
        fund_id = self.fund_id_entry.text()

        try:
            print(f"Sending DELETE request to {BASE_URL}/funds/{fund_id}")
            response = requests.delete(f"{BASE_URL}/funds/{fund_id}")
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Fund deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete fund: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete fund: {e}")

    def view_fund(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Fund List", self))

        try:
            print(f"Sending GET request to {BASE_URL}/funds")
            response = requests.get(f"{BASE_URL}/funds")
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                funds = response.json()
                print("Parsed fund data:", funds)

                self.fund_table = QTableWidget()
                self.fund_table.setRowCount(len(funds))
                self.fund_table.setColumnCount(3)
                self.fund_table.setHorizontalHeaderLabels(["ID", "Name", "Amount"])
                for i, fund in enumerate(funds):
                    self.fund_table.setItem(i, 0, QTableWidgetItem(str(fund["id"])))
                    self.fund_table.setItem(i, 1, QTableWidgetItem(fund["name"]))
                    self.fund_table.setItem(i, 2, QTableWidgetItem(str(fund["amount"])))

                self.layout.addWidget(self.fund_table)
            else:
                QMessageBox.critical(self, "Error", f"Failed to fetch funds: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch funds: {e}")

        self.back_button = QPushButton("Back to Fund Management", self)
        self.back_button.clicked.connect(self.switch_to_fund_management)
        self.layout.addWidget(self.back_button)


    def switch_to_stock_management(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Stock Management", self))

        self.add_stock_button = QPushButton("Add Stock", self)
        self.add_stock_button.clicked.connect(self.add_stock)
        self.layout.addWidget(self.add_stock_button)

        self.update_stock_button = QPushButton("Update Stock", self)
        self.update_stock_button.clicked.connect(self.update_stock)
        self.layout.addWidget(self.update_stock_button)

        self.delete_stock_button = QPushButton("Delete Stock", self)
        self.delete_stock_button.clicked.connect(self.delete_stock)
        self.layout.addWidget(self.delete_stock_button)

        self.view_stocks_button = QPushButton("View Stock List", self)
        self.view_stocks_button.clicked.connect(self.view_stocks)
        self.layout.addWidget(self.view_stocks_button)

        self.back_button = QPushButton("Back to Dashboard", self)
        self.back_button.clicked.connect(self.switch_to_dashboard)
        self.layout.addWidget(self.back_button)

    def add_stock(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Add Stock", self))

        self.layout.addWidget(QLabel("Stock Name"))
        self.stock_name_entry = QLineEdit(self)
        self.layout.addWidget(self.stock_name_entry)

        self.layout.addWidget(QLabel("Stock Symbol"))
        self.stock_symbol_entry = QLineEdit(self)
        self.layout.addWidget(self.stock_symbol_entry)

        self.layout.addWidget(QLabel("Stock Price"))
        self.stock_price_entry = QLineEdit(self)
        self.layout.addWidget(self.stock_price_entry)

        self.add_stock_submit_button = QPushButton("Add Stock", self)
        self.add_stock_submit_button.clicked.connect(self.handle_add_stock)
        self.layout.addWidget(self.add_stock_submit_button)

        self.back_button = QPushButton("Back to Stock Management", self)
        self.back_button.clicked.connect(self.switch_to_stock_management)
        self.layout.addWidget(self.back_button)

    def handle_add_stock(self):
        stock_name = self.stock_name_entry.text()
        stock_symbol = self.stock_symbol_entry.text()
        stock_price = self.stock_price_entry.text()

        payload = {
            "name": stock_name,
            "symbol": stock_symbol,
            "price": stock_price
        }

        try:
            print(f"Sending POST request to {BASE_URL}/stocks with payload: {payload}")
            response = requests.post(f"{BASE_URL}/stocks", json=payload)
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Stock added successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to add stock: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add stock: {e}")

    def update_stock(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Update Stock", self))

        self.layout.addWidget(QLabel("Stock ID"))
        self.stock_id_entry = QLineEdit(self)
        self.layout.addWidget(self.stock_id_entry)

        self.layout.addWidget(QLabel("New Stock Name"))
        self.stock_name_entry = QLineEdit(self)
        self.layout.addWidget(self.stock_name_entry)

        self.layout.addWidget(QLabel("New Stock Symbol"))
        self.stock_symbol_entry = QLineEdit(self)
        self.layout.addWidget(self.stock_symbol_entry)

        self.layout.addWidget(QLabel("New Stock Price"))
        self.stock_price_entry = QLineEdit(self)
        self.layout.addWidget(self.stock_price_entry)

        self.update_stock_submit_button = QPushButton("Update Stock", self)
        self.update_stock_submit_button.clicked.connect(self.handle_update_stock)
        self.layout.addWidget(self.update_stock_submit_button)

        self.back_button = QPushButton("Back to Stock Management", self)
        self.back_button.clicked.connect(self.switch_to_stock_management)
        self.layout.addWidget(self.back_button)

    def handle_update_stock(self):
        stock_id = self.stock_id_entry.text()
        stock_name = self.stock_name_entry.text()
        stock_symbol = self.stock_symbol_entry.text()
        stock_price = self.stock_price_entry.text()

        payload = {
            "name": stock_name,
            "symbol": stock_symbol,
            "price": stock_price
        }

        try:
            print(f"Sending PUT request to {BASE_URL}/stocks/{stock_id} with payload: {payload}")
            response = requests.put(f"{BASE_URL}/stocks/{stock_id}", json=payload)
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Stock updated successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to update stock: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update stock: {e}")

    def delete_stock(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Delete Stock", self))

        self.layout.addWidget(QLabel("Stock ID"))
        self.stock_id_entry = QLineEdit(self)
        self.layout.addWidget(self.stock_id_entry)

        self.delete_stock_submit_button = QPushButton("Delete Stock", self)
        self.delete_stock_submit_button.clicked.connect(self.handle_delete_stock)
        self.layout.addWidget(self.delete_stock_submit_button)

        self.back_button = QPushButton("Back to Stock Management", self)
        self.back_button.clicked.connect(self.switch_to_stock_management)
        self.layout.addWidget(self.back_button)

    def handle_delete_stock(self):
        stock_id = self.stock_id_entry.text()

        try:
            print(f"Sending DELETE request to {BASE_URL}/stocks/{stock_id}")
            response = requests.delete(f"{BASE_URL}/stocks/{stock_id}")
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Stock deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete stock: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete stock: {e}")

    def view_stocks(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Stock List", self))

        try:
            print(f"Sending GET request to {BASE_URL}/stocks")
            response = requests.get(f"{BASE_URL}/stocks")
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                stocks = response.json()
                print("Parsed stock data:", stocks)

                self.stock_table = QTableWidget()
                self.stock_table.setRowCount(len(stocks))
                self.stock_table.setColumnCount(4)
                self.stock_table.setHorizontalHeaderLabels(["ID", "Name", "Symbol", "Price"])
                for i, stock in enumerate(stocks):
                    self.stock_table.setItem(i, 0, QTableWidgetItem(str(stock["id"])))
                    self.stock_table.setItem(i, 1, QTableWidgetItem(stock["name"]))
                    self.stock_table.setItem(i, 2, QTableWidgetItem(stock["symbol"]))
                    self.stock_table.setItem(i, 3, QTableWidgetItem(str(stock["price"])))

                self.layout.addWidget(self.stock_table)
            else:
                QMessageBox.critical(self, "Error", f"Failed to fetch stocks: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch stocks: {e}")

        self.back_button = QPushButton("Back to Stock Management", self)
        self.back_button.clicked.connect(self.switch_to_stock_management)
        self.layout.addWidget(self.back_button)

    def switch_to_user_management(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("User Management", self))

        self.view_users_button = QPushButton("View Users", self)
        self.view_users_button.clicked.connect(self.view_users)
        self.layout.addWidget(self.view_users_button)

        self.update_user_button = QPushButton("Update User", self)
        self.update_user_button.clicked.connect(self.update_user)
        self.layout.addWidget(self.update_user_button)

        self.delete_user_button = QPushButton("Delete User", self)
        self.delete_user_button.clicked.connect(self.delete_user)
        self.layout.addWidget(self.delete_user_button)

        self.back_button = QPushButton("Back to Dashboard", self)
        self.back_button.clicked.connect(self.switch_to_dashboard)
        self.layout.addWidget(self.back_button)

    def view_users(self):
        self.clear_layout()
        
        self.layout.addWidget(QLabel("User List", self))

        try:
            print(f"Sending GET request to {BASE_URL}/users")
            response = requests.get(f"{BASE_URL}/users")
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                users = response.json()
                print("Parsed user data:", users)

                self.user_table = QTableWidget()
                self.user_table.setRowCount(len(users))
                self.user_table.setColumnCount(2)
                self.user_table.setHorizontalHeaderLabels(["Username", "Password"])
                for i, user in enumerate(users):
                    self.user_table.setItem(i, 0, QTableWidgetItem(user[0]))
                    self.user_table.setItem(i, 1, QTableWidgetItem(user[1]))
                    
                self.layout.addWidget(self.user_table)
            else:
                QMessageBox.critical(self, "Error", f"Failed to fetch users: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch users: {e}")

        self.back_button = QPushButton("Back to User Management", self)
        self.back_button.clicked.connect(self.switch_to_user_management)
        self.layout.addWidget(self.back_button)

    def update_user(self):
        self.clear_layout()
        
        self.layout.addWidget(QLabel("Update User", self))

        self.layout.addWidget(QLabel("User ID"))
        self.user_id_entry = QLineEdit(self)
        self.layout.addWidget(self.user_id_entry)
        
        self.layout.addWidget(QLabel("New Email"))
        self.user_email_entry = QLineEdit(self)
        self.layout.addWidget(self.user_email_entry)

        self.layout.addWidget(QLabel("New Phone"))
        self.user_phone_entry = QLineEdit(self)
        self.layout.addWidget(self.user_phone_entry)
        
        self.layout.addWidget(QLabel("New Address"))
        self.user_address_entry = QLineEdit(self)
        self.layout.addWidget(self.user_address_entry)
        
        self.update_user_submit_button = QPushButton("Update User", self)
        self.update_user_submit_button.clicked.connect(self.handle_update_user)
        self.layout.addWidget(self.update_user_submit_button)

        self.back_button = QPushButton("Back to User Management", self)
        self.back_button.clicked.connect(self.switch_to_user_management)
        self.layout.addWidget(self.back_button)

    def handle_update_user(self):
        user_id = self.user_id_entry.text()
        email = self.user_email_entry.text()
        phone = self.user_phone_entry.text()
        address = self.user_address_entry.text()

        payload = {
            "email": email,
            "phone": phone,
            "address": address
        }

        try:
            print(f"Sending PUT request to {BASE_URL}/users/{user_id} with payload: {payload}")
            response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "User updated successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to update user: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update user: {e}")

    def delete_user(self):
        self.clear_layout()

        self.layout.addWidget(QLabel("Delete User", self))

        self.layout.addWidget(QLabel("User ID"))
        self.user_id_entry = QLineEdit(self)
        self.layout.addWidget(self.user_id_entry)
        
        self.delete_user_submit_button = QPushButton("Delete User", self)
        self.delete_user_submit_button.clicked.connect(self.handle_delete_user)
        self.layout.addWidget(self.delete_user_submit_button)

        self.back_button = QPushButton("Back to User Management", self)
        self.back_button.clicked.connect(self.switch_to_user_management)
        self.layout.addWidget(self.back_button)

    def handle_delete_user(self):
        user_id = self.user_id_entry.text()

        try:
            print(f"Sending DELETE request to {BASE_URL}/users/{user_id}")
            response = requests.delete(f"{BASE_URL}/users/{user_id}")
            print(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "User deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete user: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete user: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())