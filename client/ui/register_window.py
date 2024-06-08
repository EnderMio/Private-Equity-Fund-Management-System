from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QMessageBox
import requests
from PyQt5.QtCore import Qt
from config import BASE_URL

class RegisterWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addWidget(QLabel("Username"))
        self.username_entry = QLineEdit(self)
        layout.addWidget(self.username_entry)

        layout.addWidget(QLabel("Password"))
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.parent.initUI)
        layout.addWidget(self.back_button)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def handle_register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        payload = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(f"{BASE_URL}/register", json=payload)

            if response.status_code == 201:
                QMessageBox.information(self, "Success", "User registered successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to register user: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to register user: {e}")
