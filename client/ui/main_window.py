from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
import requests
from .login_window import LoginWindow  # 假设此处有一个登录窗口
from .register_window import RegisterWindow  # 假设此处有一个注册窗口
from .dashboard import Dashboard  # 假设此处有一个仪表板窗口

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("私募基金管理系统")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 创建 session 对象
        self.session = requests.Session()

        self.initUI()

    def initUI(self):
        self.clear_layout()

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.label = QLabel("欢迎使用私募基金管理系统", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.choice_label = QLabel("请选择一个选项:", self)
        self.choice_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.choice_label)

        self.login_button = QPushButton("登录", self)
        self.login_button.clicked.connect(self.switch_to_login)
        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("注册", self)
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
        print(f"切换到用户的仪表板: {username}")  # 调试信息
        self.clear_layout()
        self.dashboard = Dashboard(self, username)  # 传递 session 对象和用户名
        self.layout.addWidget(self.dashboard)
        print("仪表板已添加到布局。")  # 调试信息