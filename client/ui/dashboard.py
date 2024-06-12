from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from .fund_management import FundManagement
from .stock_management import StockManagement
from .user_management import UserManagement

class Dashboard(QWidget):
    def __init__(self, parent, username, role):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.session = parent.session
        self.user_role = role
        self.initUI()
        self.load_styles()

    def initUI(self):
        print("初始化仪表板 UI...")  # 调试信息
        layout = QGridLayout()
        self.setLayout(layout)

        # 创建一个顶部布局，并放置两个标签
        top_layout = QHBoxLayout()
        top_layout.setSpacing(0)
        top_layout.setContentsMargins(10, 10, 10, 10)

        self.welcome_label = QLabel(f"欢迎，{self.username}!", self)
        self.welcome_label.setObjectName("welcomeLabel")
        top_layout.addWidget(self.welcome_label, alignment=Qt.AlignLeft)

        top_layout.addStretch(1)

        self.module_label = QLabel("基金管理", self)
        self.module_label.setObjectName("moduleLabel")
        top_layout.addWidget(self.module_label, alignment=Qt.AlignRight)

        # 将顶部布局添加到一个垂直布局中
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # 将顶部布局放置在网格布局中
        layout.addWidget(top_widget, 0, 0, 1, 3, alignment=Qt.AlignTop)
        # 添加分割线
        vline = QFrame()
        vline.setObjectName("vline")
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Sunken)
        layout.addWidget(vline, 1, 1, 2, 1)  # 垂直分割线，位置调整为 (1, 1, 2, 1)

        # 左侧菜单布局
        side_menu = QVBoxLayout()
        side_menu.setSpacing(20)  # 按钮之间的间距
        buttons = [
            QPushButton("基金管理", self, clicked=lambda: self.display_page(self.fund_management, "基金管理")),
            QPushButton("股票管理", self, clicked=lambda: self.display_page(self.stock_management, "股票管理")),
            QPushButton("用户管理", self, clicked=lambda: self.display_page(self.user_management, "用户管理")),
            QPushButton("登出", self, clicked=self.parent.initUI)
        ]
        for button in buttons:
            side_menu.addWidget(button)
        layout.addLayout(side_menu, 1, 0, 2, 1, alignment=Qt.AlignTop)  # 将按钮居中对齐

        # 右侧内容区
        self.content_area = QStackedWidget(self)
        self.content_area.setStyleSheet("margin: 10px;")
        layout.addWidget(self.content_area, 1, 2, 2, 1)  # 位置调整为 (1, 2, 2, 1)

        # 添加内容页面
        self.fund_management = FundManagement(self)
        self.content_area.addWidget(self.fund_management)

        self.stock_management = StockManagement(self)
        self.content_area.addWidget(self.stock_management)

        self.user_management = UserManagement(self)
        self.content_area.addWidget(self.user_management)

        print("仪表板 UI 初始化成功。")  # 调试信息

    def display_page(self, page, title):
        index = self.content_area.indexOf(page)
        if index != -1:
            self.content_area.setCurrentIndex(index)
            self.module_label.setText(title)  # 更新模块标题
            print(f"显示页面: {page}")
        else:
            print(f"页面 {page} 未在QStackedWidget中找到")

    def load_styles(self):
        with open("styles.qss", "r") as file:
            self.setStyleSheet(file.read())
