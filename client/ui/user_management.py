from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem
import requests
from config import BASE_URL

class UserManagement(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        print("Initializing UserManagement...")  # 调试信息
        self.parent = parent
        self.initUI()
        print("UserManagement initialized successfully.")  # 调试信息

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("User Management", self))

        self.view_users_button = QPushButton("View Users", self)
        self.view_users_button.clicked.connect(self.view_users)
        layout.addWidget(self.view_users_button)

        self.update_user_button = QPushButton("Update User", self)
        self.update_user_button.clicked.connect(self.update_user)
        layout.addWidget(self.update_user_button)

        self.delete_user_button = QPushButton("Delete User", self)
        self.delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(self.delete_user_button)

    # 其他方法保持不变

    def clear_layout(self):
        while self.layout().count():  # 清空布局中的所有组件
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


    def view_users(self):
        self.clear_layout()  # 清空当前布局
        layout = QVBoxLayout()  # 重新设置布局
        self.setLayout(layout)
        
        layout.addWidget(QLabel("User List", self))

        try:
            response = requests.get(f"{BASE_URL}/users")

            if response.status_code == 200:
                users = response.json()

                self.user_table = QTableWidget()
                self.user_table.setRowCount(len(users))
                self.user_table.setColumnCount(2)
                self.user_table.setHorizontalHeaderLabels(["Username", "Password"])
                for i, user in enumerate(users):
                    self.user_table.setItem(i, 0, QTableWidgetItem(user["username"]))
                    self.user_table.setItem(i, 1, QTableWidgetItem(user["password"]))
                    
                layout.addWidget(self.user_table)
            else:
                QMessageBox.critical(self, "Error", f"Failed to fetch users: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch users: {e}")

        self.back_button = QPushButton("Back to User Management", self)
        self.back_button.clicked.connect(self.initUI)
        layout.addWidget(self.back_button)

    def update_user(self):
        self.clear_layout()  # 清空当前布局
        layout = QVBoxLayout()  # 重新设置布局
        self.setLayout(layout)
        
        layout.addWidget(QLabel("Update User", self))

        layout.addWidget(QLabel("User ID"))
        self.user_id_entry = QLineEdit(self)
        layout.addWidget(self.user_id_entry)
        
        layout.addWidget(QLabel("New Email"))
        self.user_email_entry = QLineEdit(self)
        layout.addWidget(self.user_email_entry)

        layout.addWidget(QLabel("New Phone"))
        self.user_phone_entry = QLineEdit(self)
        layout.addWidget(self.user_phone_entry)
        
        layout.addWidget(QLabel("New Address"))
        self.user_address_entry = QLineEdit(self)
        layout.addWidget(self.user_address_entry)
        
        self.update_user_submit_button = QPushButton("Update User", self)
        self.update_user_submit_button.clicked.connect(self.handle_update_user)
        layout.addWidget(self.update_user_submit_button)

        self.back_button = QPushButton("Back to User Management", self)
        self.back_button.clicked.connect(self.initUI)
        layout.addWidget(self.back_button)

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
            response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "User updated successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to update user: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update user: {e}")

    def delete_user(self):
        self.clear_layout()  # 清空当前布局
        layout = QVBoxLayout()  # 重新设置布局
        self.setLayout(layout)

        layout.addWidget(QLabel("Delete User", self))

        layout.addWidget(QLabel("User ID"))
        self.user_id_entry = QLineEdit(self)
        layout.addWidget(self.user_id_entry)
        
        self.delete_user_submit_button = QPushButton("Delete User", self)
        self.delete_user_submit_button.clicked.connect(self.handle_delete_user)
        layout.addWidget(self.delete_user_submit_button)

        self.back_button = QPushButton("Back to User Management", self)
        self.back_button.clicked.connect(self.initUI)
        layout.addWidget(self.back_button)

    def handle_delete_user(self):
        user_id = self.user_id_entry.text()

        try:
            response = requests.delete(f"{BASE_URL}/users/{user_id}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "User deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete user: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete user: {e}")