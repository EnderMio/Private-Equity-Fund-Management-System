# login_window.py
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt
from config import BASE_URL

class LoginWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.session = requests.Session()  # 初始化会话
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

        self.login_button = QPushButton("登录", self)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.back_button = QPushButton("返回", self)
        self.back_button.clicked.connect(self.parent.initUI)
        layout.addWidget(self.back_button)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def handle_login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        payload = {
            "username": username,
            "password": password
        }

        try:
            response = self.session.post(f"{BASE_URL}/login", json=payload)  # 使用会话对象发送请求
            response.raise_for_status()  # Raise an exception for HTTP errors

            if response.status_code == 200:
                user_data = response.json()
                user_role = user_data.get('role')
                if user_role:
                    QMessageBox.information(self, "成功", "登录成功！")
                    self.parent.session = self.session  # 保存会话对象到父组件
                    self.parent.switch_to_dashboard(username, user_role)
                else:
                    QMessageBox.critical(self, "错误", "获取用户信息失败")
            else:
                QMessageBox.critical(self, "错误", f"登录失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"登录失败: {e}")
