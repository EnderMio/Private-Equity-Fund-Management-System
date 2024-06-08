from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit, QScrollArea, QFormLayout, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
import requests
from config import BASE_URL
from .fund_fields import create_form_layout, fields

class FundManagement(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        print("正在初始化基金管理...")  # 调试信息
        self.session = parent.session  # 使用父组件的会话对象
        self.parent = parent
        self.scroll_area = None  # 初始化 scroll_area
        self.initUI()
        print("基金管理初始化成功。")  # 调试信息

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_fund_button = QPushButton("创建基金", self)
        self.create_fund_button.clicked.connect(self.show_create_fund)
        self.layout.addWidget(self.create_fund_button)

        self.update_fund_button = QPushButton("更新基金", self)
        self.update_fund_button.clicked.connect(self.show_update_fund)
        self.layout.addWidget(self.update_fund_button)

        self.delete_fund_button = QPushButton("删除基金", self)
        self.delete_fund_button.clicked.connect(self.show_delete_fund)
        self.layout.addWidget(self.delete_fund_button)

        self.view_fund_button = QPushButton("查看基金详情", self)
        self.view_fund_button.clicked.connect(self.show_view_fund)
        self.layout.addWidget(self.view_fund_button)

        self.create_fund_layout = None
        self.update_fund_layout = None
        self.delete_fund_layout = None
        self.view_fund_layout = None

    def show_create_fund(self):
        self.clear_content()
        self.scroll_area = QScrollArea(self)
        self.layout.addWidget(self.scroll_area)

        container = QWidget()
        form_layout = QFormLayout(container)
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        required_fields = [
            "基金名称",
            "基金描述",
            "基金金额",
            "基金经理",
            "基金类型",
            "费用率",
            "风险等级",
        ]

        self.entries = {}

        for label in required_fields:
            field_name = fields[label]
            entry = QLineEdit(self)
            form_layout.addRow(QLabel(label), entry)
            self.entries[field_name] = entry

        self.create_fund_submit_button = QPushButton("创建基金", self)
        self.create_fund_submit_button.clicked.connect(self.handle_create_fund)
        form_layout.addWidget(self.create_fund_submit_button)

        self.back_button = QPushButton("返回基金管理", self)
        self.back_button.clicked.connect(self.clear_content)
        form_layout.addWidget(self.back_button)


    def handle_create_fund(self):
        name = self.entries['name'].text()
        description = self.entries['description'].text()
        amount = self.entries['amount'].text()
        manager = self.entries['manager'].text()
        type = self.entries['type'].text()
        expense_ratio = self.entries['expense_ratio'].text()
        risk_level = self.entries['risk_level'].text()

        payload = {
            "name": name,
            "description": description,
            "amount": amount,
            "manager": manager,
            "type": type,
            "expense_ratio": expense_ratio,
            "risk_level": risk_level
        }

        try:
            print(f"发送请求到 {BASE_URL}/funds，负载: {payload}")  # 调试信息
            response = self.session.post(f"{BASE_URL}/funds", json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

            print(f"接收到响应: {response.status_code} - {response.text}")  # 调试信息

            if response.status_code == 201:
                QMessageBox.information(self, "成功", "基金创建成功！")
            else:
                QMessageBox.critical(self, "错误", f"创建基金失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建基金失败: {e}")

    
    def show_update_fund(self):
        self.clear_content()
        self.update_fund_layout, self.entries = create_form_layout(self)
        self.layout.addLayout(self.update_fund_layout)

        self.update_fund_layout.addWidget(QLabel("基金ID"))
        self.entries['id'] = QLineEdit(self)
        self.update_fund_layout.addWidget(self.entries['id'])

        self.update_fund_submit_button = QPushButton("更新基金", self)
        self.update_fund_submit_button.clicked.connect(self.handle_update_fund)
        self.update_fund_layout.addWidget(self.update_fund_submit_button)

        self.back_button = QPushButton("返回基金管理", self)
        self.back_button.clicked.connect(self.clear_content)
        self.update_fund_layout.addWidget(self.back_button)

    def handle_update_fund(self):
        payload = {field_name: entry.text() for field_name, entry in self.entries.items()}
        fund_id = payload.pop("id")

        try:
            response = self.session.put(f"{BASE_URL}/funds/{fund_id}", json=payload)

            if response.status_code == 200:
                QMessageBox.information(self, "成功", "基金更新成功！")
            else:
                QMessageBox.critical(self, "错误", f"更新基金失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"更新基金失败: {e}")

    def show_delete_fund(self):
        self.clear_content()
        self.delete_fund_layout = QVBoxLayout()
        self.layout.addLayout(self.delete_fund_layout)

        self.delete_fund_layout.addWidget(QLabel("删除基金", self))

        self.delete_fund_layout.addWidget(QLabel("基金ID"))
        self.fund_id_entry = QLineEdit(self)
        self.delete_fund_layout.addWidget(self.fund_id_entry)

        self.delete_fund_submit_button = QPushButton("删除基金", self)
        self.delete_fund_submit_button.clicked.connect(self.handle_delete_fund)
        self.delete_fund_layout.addWidget(self.delete_fund_submit_button)

        self.back_button = QPushButton("返回基金管理", self)
        self.back_button.clicked.connect(self.clear_content)
        self.delete_fund_layout.addWidget(self.back_button)

    def handle_delete_fund(self):
        fund_id = self.fund_id_entry.text()

        try:
            response = self.session.delete(f"{BASE_URL}/funds/{fund_id}")

            if response.status_code == 200:
                QMessageBox.information(self, "成功", "基金删除成功！")
            else:
                QMessageBox.critical(self, "错误", f"删除基金失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除基金失败: {e}")

    def show_view_fund(self):
        self.clear_content()
        self.view_fund_layout = QVBoxLayout()
        self.layout.addLayout(self.view_fund_layout)

        self.view_fund_layout.addWidget(QLabel("基金列表", self))

        try:
            response = self.session.get(f"{BASE_URL}/funds")

            if response.status_code == 200:
                funds = response.json()

                self.fund_table = QTableWidget()
                self.fund_table.setRowCount(len(funds))
                self.fund_table.setColumnCount(len(fields) + 1)  # 加上 ID 列

                # 设置表头标签
                header_labels = ["ID"] + list(fields.values())
                print(f"表头标签: {header_labels}")  # 调试信息
                self.fund_table.setHorizontalHeaderLabels(header_labels)

                headers = ['id'] + list(fields.values())

                for i, fund in enumerate(funds):
                    for j, header in enumerate(headers):
                        value = fund.get(header, "")
                        if header == 'fund_inception_date' and value:
                            value = value[:10]  # 只取日期部分
                        self.fund_table.setItem(i, j, QTableWidgetItem(str(value)))

                # 设置表头可见
                self.fund_table.horizontalHeader().setVisible(True)
                self.fund_table.verticalHeader().setVisible(True)

                # 设置表格内容不可编辑
                self.fund_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                # 启用水平和垂直滚动
                self.fund_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                self.fund_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

                self.view_fund_layout.addWidget(self.fund_table)

                # 调试信息，检查设置的表头
                for i in range(self.fund_table.columnCount()):
                    header_item = self.fund_table.horizontalHeaderItem(i)
                    if header_item:
                        print(f"表头第 {i} 列: {header_item.text()}")
                    else:
                        print(f"表头第 {i} 列: 无")

            else:
                QMessageBox.critical(self, "错误", f"获取基金列表失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取基金列表失败: {e}")

        self.back_button = QPushButton("返回基金管理", self)
        self.back_button.clicked.connect(self.clear_content)
        self.view_fund_layout.addWidget(self.back_button)



    def clear_content(self):
        if self.create_fund_layout:
            while self.create_fund_layout.count():
                item = self.create_fund_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.create_fund_layout = None
        if self.update_fund_layout:
            while self.update_fund_layout.count():
                item = self.update_fund_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.update_fund_layout = None
        if self.delete_fund_layout:
            while self.delete_fund_layout.count():
                item = self.delete_fund_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.delete_fund_layout = None
        if self.view_fund_layout:
            while self.view_fund_layout.count():
                item = self.view_fund_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.view_fund_layout = None
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.scroll_area.deleteLater()
            self.scroll_area = None

        self.layout.setAlignment(Qt.AlignTop)

