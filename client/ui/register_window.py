from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QMessageBox
import requests
from PyQt5.QtCore import Qt
from config import BASE_URL
import re
from PyQt5.QtWidgets import QMessageBox

class RegisterWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addWidget(QLabel("用户名"))
        self.username_entry = QLineEdit(self)
        layout.addWidget(self.username_entry)

        layout.addWidget(QLabel("密码"))
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        self.register_button = QPushButton("注册", self)
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.back_button = QPushButton("返回", self)
        self.back_button.clicked.connect(self.parent.initUI)
        layout.addWidget(self.back_button)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def handle_register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        # 检查密码长度
        if len(password) < 8:
            QMessageBox.critical(self, "失败", "密码长度必须至少为8个字符")
            return

        # 检查密码复杂度（至少包含一个大写字母、一个小写字母和一个数字）
        if not re.search(r'[A-Z]', password):
            QMessageBox.critical(self, "失败", "密码必须包含至少一个大写字母")
            return
        if not re.search(r'[a-z]', password):
            QMessageBox.critical(self, "失败", "密码必须包含至少一个小写字母")
            return
        if not re.search(r'[0-9]', password):
            QMessageBox.critical(self, "失败", "密码必须包含至少一个数字")
            return
        if not re.search(r'[!@#\$%\^&\*]', password):
            QMessageBox.critical(self, "失败", "密码必须包含至少一个特殊字符 !@#$%^&*")
            return

        payload = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(f"{BASE_URL}/register", json=payload)

            if response.status_code == 201:
                QMessageBox.information(self, "成功", "用户注册成功!")
            else:
                QMessageBox.critical(self, "失败", f"创建用户失败: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "失败", f"创建用户失败: {e}")
