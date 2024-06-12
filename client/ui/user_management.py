from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QFormLayout, QScrollArea, QHeaderView
from PyQt5.QtCore import Qt
import requests
from config import BASE_URL

class UserManagement(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.session = parent.session  # 使用父组件的会话对象
        self.scroll_area = None  # 初始化 scroll_area
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.update_user_button = QPushButton("更新用户", self)
        self.update_user_button.clicked.connect(self.show_update_user)
        self.layout.addWidget(self.update_user_button)

        self.delete_user_button = QPushButton("删除用户", self)
        self.delete_user_button.clicked.connect(self.show_delete_user)
        self.layout.addWidget(self.delete_user_button)

        self.view_users_button = QPushButton("查看用户详情", self)
        self.view_users_button.clicked.connect(self.show_view_users)
        self.layout.addWidget(self.view_users_button)

        self.update_user_layout = None
        self.delete_user_layout = None
        self.view_users_layout = None

    def clear_content(self):
        if self.update_user_layout:
            while self.update_user_layout.count():
                item = self.update_user_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.update_user_layout = None
        if self.delete_user_layout:
            while self.delete_user_layout.count():
                item = self.delete_user_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.delete_user_layout = None
        if self.view_users_layout:
            while self.view_users_layout.count():
                item = self.view_users_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.view_users_layout = None
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.scroll_area.deleteLater()
            self.scroll_area = None

        self.layout.setAlignment(Qt.AlignTop)

    def show_update_user(self):
        self.clear_content()
        self.scroll_area = QScrollArea(self)
        self.layout.addWidget(self.scroll_area)

        container = QWidget()
        form_layout = QFormLayout(container)
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        self.user_id_entry = QLineEdit(self)
        self.new_username_entry = QLineEdit(self)
        self.new_password_entry = QLineEdit(self)
        self.new_role_entry = QLineEdit(self)

        form_layout.addRow(QLabel("用户ID"), self.user_id_entry)
        form_layout.addRow(QLabel("新用户名"), self.new_username_entry)
        form_layout.addRow(QLabel("新密码"), self.new_password_entry)
        form_layout.addRow(QLabel("新角色"), self.new_role_entry)

        self.update_user_submit_button = QPushButton("更新用户", self)
        self.update_user_submit_button.clicked.connect(self.handle_update_user)
        form_layout.addWidget(self.update_user_submit_button)

        self.back_button = QPushButton("返回用户管理", self)
        self.back_button.clicked.connect(self.clear_content)
        form_layout.addWidget(self.back_button)

    def handle_update_user(self):
        user_id = self.user_id_entry.text()
        new_username = self.new_username_entry.text()
        new_password = self.new_password_entry.text()
        new_role = self.new_role_entry.text()

        payload = {
            "username": new_username,
            "password": new_password,
            "role": new_role
        }

        try:
            response = self.session.put(f"{BASE_URL}/users/{user_id}", json=payload)
            response.raise_for_status()
            QMessageBox.information(self, "成功", "用户更新成功！")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"更新用户失败: {e}")

    def show_delete_user(self):
        self.clear_content()
        self.scroll_area = QScrollArea(self)
        self.layout.addWidget(self.scroll_area)

        container = QWidget()
        form_layout = QFormLayout(container)
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        self.user_id_entry = QLineEdit(self)

        form_layout.addRow(QLabel("用户ID"), self.user_id_entry)

        self.delete_user_submit_button = QPushButton("删除用户", self)
        self.delete_user_submit_button.clicked.connect(self.handle_delete_user)
        form_layout.addWidget(self.delete_user_submit_button)

        self.back_button = QPushButton("返回用户管理", self)
        self.back_button.clicked.connect(self.clear_content)
        form_layout.addWidget(self.back_button)

    def handle_delete_user(self):
        user_id = self.user_id_entry.text()

        try:
            response = self.session.delete(f"{BASE_URL}/users/{user_id}")
            response.raise_for_status()
            QMessageBox.information(self, "成功", "用户删除成功！")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"删除用户失败: {e}")

    def show_view_users(self):
        self.clear_content()
        self.scroll_area = QScrollArea(self)
        self.layout.addWidget(self.scroll_area)

        container = QWidget()
        layout = QVBoxLayout(container)
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        layout.addWidget(QLabel("用户列表", self))
        
        

        try:
            response = self.session.get(f"{BASE_URL}/users")
            response.raise_for_status()
            users = response.json()

            self.user_table = QTableWidget()
            self.user_table.setRowCount(len(users))
            self.user_table.setColumnCount(3)
            self.user_table.setHorizontalHeaderLabels(["ID", "用户名", "角色"])
            
            self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.user_table.horizontalHeader().setStretchLastSection(True)
            self.user_table.horizontalHeader().setFixedHeight(50)

            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
                self.user_table.setItem(row, 1, QTableWidgetItem(user['username']))
                self.user_table.setItem(row, 2, QTableWidgetItem(user['role']))

            layout.addWidget(self.user_table)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"获取用户列表失败: {e}")

        self.back_button = QPushButton("返回用户管理", self)
        self.back_button.clicked.connect(self.clear_content)
        layout.addWidget(self.back_button)
