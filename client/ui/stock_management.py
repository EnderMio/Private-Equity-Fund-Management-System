from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit, QScrollArea, QFormLayout, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
import requests
from config import BASE_URL
from .stock_fields import create_stock_form_layout, stock_fields

class StockManagement(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        print("正在初始化股票管理...")  # 调试信息
        self.session = parent.session  # 使用父组件的会话对象
        self.parent = parent
        self.scroll_area = None  # 初始化 scroll_area
        self.initUI()
        print("股票管理初始化成功。")  # 调试信息

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_stock_button = QPushButton("创建股票", self)
        self.create_stock_button.clicked.connect(self.show_create_stock)
        self.layout.addWidget(self.create_stock_button)

        self.update_stock_button = QPushButton("更新股票", self)
        self.update_stock_button.clicked.connect(self.show_update_stock)
        self.layout.addWidget(self.update_stock_button)

        self.delete_stock_button = QPushButton("删除股票", self)
        self.delete_stock_button.clicked.connect(self.show_delete_stock)
        self.layout.addWidget(self.delete_stock_button)

        self.view_stock_button = QPushButton("查看股票列表", self)
        self.view_stock_button.clicked.connect(self.show_view_stock)
        self.layout.addWidget(self.view_stock_button)

        self.create_stock_layout = None
        self.update_stock_layout = None
        self.delete_stock_layout = None
        self.view_stock_layout = None

    def show_create_stock(self):
        self.clear_content()
        self.scroll_area = QScrollArea(self)
        self.layout.addWidget(self.scroll_area)

        container = QWidget()
        form_layout = QFormLayout(container)
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)

        required_fields = [
            "股票名称",
            "股票符号",
            "股票价格",
            "行业"
        ]

        self.entries = {}

        for label in required_fields:
            field_name = stock_fields[label]
            entry = QLineEdit(self)
            form_layout.addRow(QLabel(label), entry)
            self.entries[field_name] = entry

        self.create_stock_submit_button = QPushButton("创建股票", self)
        self.create_stock_submit_button.clicked.connect(self.handle_create_stock)
        form_layout.addWidget(self.create_stock_submit_button)

        self.back_button = QPushButton("返回股票管理", self)
        self.back_button.clicked.connect(self.clear_content)
        form_layout.addWidget(self.back_button)

    def handle_create_stock(self):
        payload = {field_name: entry.text() for field_name, entry in self.entries.items()}

        try:
            print(f"发送请求到 {BASE_URL}/stocks，负载: {payload}")  # 调试信息
            response = self.session.post(f"{BASE_URL}/stocks", json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

            print(f"接收到响应: {response.status_code} - {response.text}")  # 调试信息

            if response.status_code == 201:
                QMessageBox.information(self, "成功", "股票创建成功！")
            else:
                QMessageBox.critical(self, "错误", f"创建股票失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建股票失败: {e}")

    def show_update_stock(self):
        self.clear_content()
        self.update_stock_layout, self.entries = create_stock_form_layout(self)
        self.layout.addLayout(self.update_stock_layout)

        self.update_stock_layout.addWidget(QLabel("股票ID"))
        self.entries['id'] = QLineEdit(self)
        self.update_stock_layout.addWidget(self.entries['id'])

        self.update_stock_submit_button = QPushButton("更新股票", self)
        self.update_stock_submit_button.clicked.connect(self.handle_update_stock)
        self.update_stock_layout.addWidget(self.update_stock_submit_button)

        self.back_button = QPushButton("返回股票管理", self)
        self.back_button.clicked.connect(self.clear_content)
        self.update_stock_layout.addWidget(self.back_button)

    def handle_update_stock(self):
        payload = {field_name: entry.text() for field_name, entry in self.entries.items()}
        stock_id = payload.pop("id")

        try:
            response = self.session.put(f"{BASE_URL}/stocks/{stock_id}", json=payload)

            if response.status_code == 200:
                QMessageBox.information(self, "成功", "股票更新成功！")
            else:
                QMessageBox.critical(self, "错误", f"更新股票失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"更新股票失败: {e}")

    def show_delete_stock(self):
        self.clear_content()
        self.delete_stock_layout = QVBoxLayout()
        self.layout.addLayout(self.delete_stock_layout)

        self.delete_stock_layout.addWidget(QLabel("删除股票", self))

        self.delete_stock_layout.addWidget(QLabel("股票ID"))
        self.stock_id_entry = QLineEdit(self)
        self.delete_stock_layout.addWidget(self.stock_id_entry)

        self.delete_stock_submit_button = QPushButton("删除股票", self)
        self.delete_stock_submit_button.clicked.connect(self.handle_delete_stock)
        self.delete_stock_layout.addWidget(self.delete_stock_submit_button)

        self.back_button = QPushButton("返回股票管理", self)
        self.back_button.clicked.connect(self.clear_content)
        self.delete_stock_layout.addWidget(self.back_button)

    def handle_delete_stock(self):
        stock_id = self.stock_id_entry.text()

        try:
            response = self.session.delete(f"{BASE_URL}/stocks/{stock_id}")

            if response.status_code == 200:
                QMessageBox.information(self, "成功", "股票删除成功！")
            else:
                QMessageBox.critical(self, "错误", f"删除股票失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除股票失败: {e}")

    def show_view_stock(self):
        self.clear_content()
        self.view_stock_layout = QVBoxLayout()
        self.layout.addLayout(self.view_stock_layout)

        self.view_stock_layout.addWidget(QLabel("股票列表", self))

        try:
            response = self.session.get(f"{BASE_URL}/stocks")

            if response.status_code == 200:
                stocks = response.json()

                self.stock_table = QTableWidget()
                self.stock_table.setRowCount(len(stocks))
                self.stock_table.setColumnCount(len(stock_fields) + 1)  # 加上 ID 列

                header_labels = ["ID"] + list(stock_fields.keys())
                self.stock_table.setHorizontalHeaderLabels(header_labels)

                headers = ['id'] + list(stock_fields.values())

                for i, stock in enumerate(stocks):
                    for j, header in enumerate(headers):
                        value = stock.get(header, "")
                        self.stock_table.setItem(i, j, QTableWidgetItem(str(value)))

                self.stock_table.horizontalHeader().setVisible(True)
                self.stock_table.verticalHeader().setVisible(True)

                # 设置表头宽度和列宽度
                self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.stock_table.horizontalHeader().setStretchLastSection(True)
                
                # 设置表头行的高度
                self.stock_table.horizontalHeader().setFixedHeight(50)

                self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.stock_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                self.stock_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

                self.view_stock_layout.addWidget(self.stock_table)
            else:
                QMessageBox.critical(self, "错误", f"获取股票列表失败: {response.json().get('message', '未知错误')}")
        except requests.exceptions.HTTPError as http_err:
            QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
        except requests.exceptions.RequestException as req_err:
            QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取股票列表失败: {e}")

        self.back_button = QPushButton("返回股票管理", self)
        self.back_button.clicked.connect(self.clear_content)
        self.view_stock_layout.addWidget(self.back_button)

    def clear_content(self):
        if self.create_stock_layout:
            while self.create_stock_layout.count():
                item = self.create_stock_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.create_stock_layout = None
        if self.update_stock_layout:
            while self.update_stock_layout.count():
                item = self.update_stock_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.update_stock_layout = None
        if self.delete_stock_layout:
            while self.delete_stock_layout.count():
                item = self.delete_stock_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.delete_stock_layout = None
        if self.view_stock_layout:
            while self.view_stock_layout.count():
                item = self.view_stock_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.view_stock_layout = None
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.scroll_area.deleteLater()
            self.scroll_area = None

        self.layout.setAlignment(Qt.AlignTop)
