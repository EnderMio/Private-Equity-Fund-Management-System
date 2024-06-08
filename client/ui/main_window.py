from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
import requests
from .login_window import LoginWindow
from .register_window import RegisterWindow
from .dashboard import Dashboard

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My PyQt App")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 创建 session 对象
        self.session = requests.Session()

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
        self.login_window = LoginWindow(self)  # 传递 session 对象
        self.layout.addWidget(self.login_window)

    def switch_to_register(self):
        self.clear_layout()
        self.register_window = RegisterWindow(self)  # 传递 session 对象
        self.layout.addWidget(self.register_window)

    def switch_to_dashboard(self, username):  # 确认此方法存在
        print(f"Switching to dashboard for user: {username}")  # 调试信息
        self.clear_layout()
        self.dashboard = Dashboard(self, username)  # 传递 session 对象和用户名
        self.layout.addWidget(self.dashboard)
        print("Dashboard added to layout.")  # 调试信息
