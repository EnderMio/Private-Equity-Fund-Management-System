from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QFormLayout, QScrollArea, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
import requests
from config import BASE_URL
from .fund_fields import fields

class UserManagement(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        print("正在初始化用户管理...")  # 调试信息
        self.session = parent.session  # 使用父组件的会话对象
        self.parent = parent
        self.scroll_area = None  # 初始化 scroll_area

        # 获取用户角色
        self.role = parent.user_role

        self.layout = QVBoxLayout()  # 初始化主布局
        self.setLayout(self.layout)
        self.initUI()
        print("用户管理初始化成功。")  # 调试信息

    def initUI(self):
        self.clear_content()

        if self.role == 'admin':
            self.update_user_button = QPushButton("更新用户", self)
            self.update_user_button.clicked.connect(self.show_update_user)
            self.layout.addWidget(self.update_user_button)

            self.delete_user_button = QPushButton("删除用户", self)
            self.delete_user_button.clicked.connect(self.show_delete_user)
            self.layout.addWidget(self.delete_user_button)

            self.view_admins_button = QPushButton("显示所有管理员", self)
            self.view_admins_button.clicked.connect(lambda: self.show_users("admin"))
            self.layout.addWidget(self.view_admins_button)

            self.view_managers_button = QPushButton("显示所有基金经理", self)
            self.view_managers_button.clicked.connect(lambda: self.show_users("manager"))
            self.layout.addWidget(self.view_managers_button)

            self.view_users_button = QPushButton("显示所有普通用户", self)
            self.view_users_button.clicked.connect(lambda: self.show_users("user"))
            self.layout.addWidget(self.view_users_button)

        elif self.role == 'manager':
            self.view_managers_button = QPushButton("显示所有基金经理", self)
            self.view_managers_button.clicked.connect(lambda: self.show_users("manager"))
            self.layout.addWidget(self.view_managers_button)

        elif self.role == 'user':
            self.view_managers_button = QPushButton("显示所有基金经理", self)
            self.view_managers_button.clicked.connect(lambda: self.show_users("manager"))
            self.layout.addWidget(self.view_managers_button)

        self.update_self_button = QPushButton("修改个人信息", self)
        self.update_self_button.clicked.connect(self.show_update_self)
        self.layout.addWidget(self.update_self_button)

    def clear_content(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

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
        self.back_button.clicked.connect(self.initUI)
        form_layout.addWidget(self.back_button)

    def handle_update_user(self):
        user_id = self.user_id_entry.text()
        new_username = self.new_username_entry.text()
        new_password = self.new_password_entry.text()
        new_role = self.new_role_entry.text()

        # 构建 payload 只包含非空字段
        payload = {}
        if new_username:
            payload['username'] = new_username
        if new_password:
            payload['password'] = new_password
        if new_role:
            payload['role'] = new_role

        if not payload:
            QMessageBox.warning(self, "警告", "没有更新的内容。")
            return

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
        self.back_button.clicked.connect(self.initUI)
        form_layout.addWidget(self.back_button)

    def handle_delete_user(self):
        user_id = self.user_id_entry.text()

        try:
            response = self.session.delete(f"{BASE_URL}/users/{user_id}")
            response.raise_for_status()
            QMessageBox.information(self, "成功", "用户删除成功！")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"删除用户失败: {e}")

    def show_users(self, role):
        self.clear_content()
        self.scroll_area = QScrollArea(self)
        self.layout.addWidget(self.scroll_area)

        container = QWidget()
        layout = QVBoxLayout(container)
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        layout.addWidget(QLabel(f"{role} 列表", self))

        try:
            response = self.session.get(f"{BASE_URL}/users?role={role}")
            response.raise_for_status()
            users = response.json()

            self.user_table = QTableWidget()
            self.user_table.setRowCount(len(users))
            self.user_table.setColumnCount(3)
            self.user_table.setHorizontalHeaderLabels(["ID", "用户名", "角色"])

            self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
            self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.user_table.horizontalHeader().setStretchLastSection(True)
            self.user_table.horizontalHeader().setFixedHeight(50)
            
            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
                self.user_table.setItem(row, 1, QTableWidgetItem(user['username']))
                self.user_table.setItem(row, 2, QTableWidgetItem(user['role']))

            if role == "manager":
                self.user_table.cellDoubleClicked.connect(self.show_manager_funds)
            layout.addWidget(self.user_table)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"获取用户列表失败: {e}")

        self.back_button = QPushButton("返回用户管理", self)
        self.back_button.clicked.connect(self.initUI)
        layout.addWidget(self.back_button)
        
    def show_manager_funds(self, row, column):
        if column == 1:  # Manager 列
            manager_username = self.user_table.item(row, column).text()
            self.clear_content()
            self.view_fund_layout = QVBoxLayout()
            self.layout.addLayout(self.view_fund_layout)

            self.view_fund_layout.addWidget(QLabel(f"{manager_username} 管理的基金列表", self))

            try:
                response = self.session.get(f"{BASE_URL}/funds/manager/{manager_username}")

                if response.status_code == 200:
                    funds = response.json()

                    self.fund_table = QTableWidget()
                    self.fund_table.setRowCount(len(funds))
                    self.fund_table.setColumnCount(len(fields) + 1)  # 加上 ID 列和 Manager 列

                    # 设置表头标签
                    header_labels = ["ID"] + list(fields.keys())
                    self.fund_table.setHorizontalHeaderLabels(header_labels)

                    headers = ['id'] + list(fields.values())

                    for i, fund in enumerate(funds):
                        for j, header in enumerate(headers):
                            if header == 'manager':
                                value = fund['manager']['username']
                            else:
                                value = fund.get(header, "")
                            if header == 'inception_date' and value:
                                value = value[:10]  # 只取日期部分
                            self.fund_table.setItem(i, j, QTableWidgetItem(str(value)))

                    # 设置表格内容不可编辑
                    self.fund_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                    self.fund_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                    self.fund_table.horizontalHeader().setStretchLastSection(True)
                    self.fund_table.horizontalHeader().setFixedHeight(50)

                    # 启用水平和垂直滚动
                    self.fund_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                    self.fund_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

                    self.fund_table.cellDoubleClicked.connect(self.show_manager_funds)

                    self.view_fund_layout.addWidget(self.fund_table)

                else:
                    QMessageBox.critical(self, "错误", f"获取基金列表失败: {response.json().get('message', '未知错误')}")
            except requests.exceptions.HTTPError as http_err:
                QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
            except requests.exceptions.RequestException as req_err:
                QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"获取基金列表失败: {e}")

            self.back_button = QPushButton("返回用户列表", self)
            self.back_button.clicked.connect(lambda: self.show_users("manager"))
            self.view_fund_layout.addWidget(self.back_button)
            
    def show_update_self(self):
        self.clear_content()
        
        self.scroll_area = QScrollArea(self)
        self.layout.addWidget(self.scroll_area)

        container = QWidget()
        form_layout = QFormLayout(container)
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        self.username_entry = QLineEdit(self)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)

        form_layout.addRow(QLabel("用户名:"), self.username_entry)
        form_layout.addRow(QLabel("密码:"), self.password_entry)

        self.update_self_submit_button = QPushButton("提交", self)
        self.update_self_submit_button.clicked.connect(self.handle_update_self)
        form_layout.addWidget(self.update_self_submit_button)

        self.back_button = QPushButton("返回用户管理", self)
        self.back_button.clicked.connect(self.initUI)
        form_layout.addWidget(self.back_button)

    def handle_update_self(self):
        new_username = self.username_entry.text()
        new_password = self.password_entry.text()

        payload = {}
        if new_username:
            payload['username'] = new_username
        if new_password:
            payload['password'] = new_password

        if not payload:
            QMessageBox.warning(self, "警告", "没有更新的内容。")
            return

        try:
            user_id = self.parent.user_id  # 假设用户ID存储在parent中
            response = self.session.put(f"{BASE_URL}/users/{user_id}", json=payload)
            response.raise_for_status()
            QMessageBox.information(self, "成功", "个人信息更新成功！")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"更新个人信息失败: {e}")