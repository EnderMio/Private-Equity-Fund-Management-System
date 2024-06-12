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
        self.role = parent.user_role
        self.scroll_area = None  # 初始化 scroll_area
        self.layout = QVBoxLayout()  # 初始化主布局
        self.setLayout(self.layout)
        self.initUI()
        print("基金管理初始化成功。")  # 调试信息

    def initUI(self):
        self.clear_content()

        if self.role == 'admin':
            self.create_fund_button = QPushButton("创建基金", self)
            self.create_fund_button.clicked.connect(self.show_create_fund)
            self.layout.addWidget(self.create_fund_button)

            self.update_fund_button = QPushButton("更新基金", self)
            self.update_fund_button.clicked.connect(self.show_update_fund)
            self.layout.addWidget(self.update_fund_button)

            self.delete_fund_button = QPushButton("删除基金", self)
            self.delete_fund_button.clicked.connect(self.show_delete_fund)
            self.layout.addWidget(self.delete_fund_button)

        if self.role in ['manager']:
            self.manage_fund_button = QPushButton("管理基金", self)
            self.manage_fund_button.clicked.connect(self.show_manage_fund)
            self.layout.addWidget(self.manage_fund_button)

        if self.role == 'user':
            self.view_user_funds_button = QPushButton("查看持有的基金", self)
            self.view_user_funds_button.clicked.connect(self.show_user_funds)
            self.layout.addWidget(self.view_user_funds_button)

        self.view_fund_button = QPushButton("查看所有基金", self)
        self.view_fund_button.clicked.connect(self.show_view_fund)
        self.layout.addWidget(self.view_fund_button)

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
        self.back_button.clicked.connect(self.initUI)
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
        self.back_button.clicked.connect(self.initUI)
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
        self.back_button.clicked.connect(self.initUI)
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

    from PyQt5.QtWidgets import QTableWidgetItem

    # def show_view_fund(self):
    #     self.clear_content()
    #     self.view_fund_layout = QVBoxLayout()
    #     self.layout.addLayout(self.view_fund_layout)

    #     self.view_fund_layout.addWidget(QLabel("基金列表", self))

    #     try:
    #         response = self.session.get(f"{BASE_URL}/funds")

    #         if response.status_code == 200:
    #             funds = response.json()

    #             self.fund_table = QTableWidget()
    #             self.fund_table.setRowCount(len(funds))
    #             self.fund_table.setColumnCount(len(fields) + 1)  # 加上 ID 列和 Manager 列

    #             # 设置表头标签
    #             header_labels = ["ID"] + list(fields.keys())
    #             self.fund_table.setHorizontalHeaderLabels(header_labels)

    #             headers = ['id'] + list(fields.values())

    #             for i, fund in enumerate(funds):
    #                 for j, header in enumerate(headers):
    #                     if header == 'manager':
    #                         value = fund['manager']['username']
    #                     else:
    #                         value = fund.get(header, "")
    #                     if header == 'inception_date' and value:
    #                         value = value[:10]  # 只取日期部分
    #                     self.fund_table.setItem(i, j, QTableWidgetItem(str(value)))

    #             # 设置表格内容不可编辑
    #             self.fund_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    #             self.fund_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #             self.fund_table.horizontalHeader().setStretchLastSection(True)
    #             self.fund_table.horizontalHeader().setFixedHeight(50)

    #             # 启用水平和垂直滚动
    #             self.fund_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    #             self.fund_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    #             self.fund_table.cellDoubleClicked.connect(self.show_manager_funds)
    #             self.fund_table.cellDoubleClicked.connect(self.show_fund_holdings)

    #             self.view_fund_layout.addWidget(self.fund_table)

    #         else:
    #             QMessageBox.critical(self, "错误", f"获取基金列表失败: {response.json().get('message', '未知错误')}")
    #     except requests.exceptions.HTTPError as http_err:
    #         QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
    #     except requests.exceptions.RequestException as req_err:
    #         QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
    #     except Exception as e:
    #         QMessageBox.critical(self, "错误", f"获取基金列表失败: {e}")

    #     self.back_button = QPushButton("返回基金管理", self)
    #     self.back_button.clicked.connect(self.initUI)
    #     self.view_fund_layout.addWidget(self.back_button)
        
    def show_fund_holdings(self, row, column):
        if column == 6:  # 持仓金额列
            fund_id = self.fund_table.item(row, 0).text()  # 获取基金ID
            self.clear_content()
            self.view_fund_layout = QVBoxLayout()
            self.layout.addLayout(self.view_fund_layout)

            self.view_fund_layout.addWidget(QLabel(f"基金ID {fund_id} 的持股列表", self))

            try:
                response = self.session.get(f"{BASE_URL}/funds/{fund_id}/holdings")

                if response.status_code == 200:
                    holdings = response.json()

                    self.holdings_table = QTableWidget()
                    self.holdings_table.setRowCount(len(holdings))
                    self.holdings_table.setColumnCount(3)  # 股票ID, 股票名称, 持股数量

                    # 设置表头标签
                    header_labels = ["股票ID", "股票名称", "持股数量"]
                    self.holdings_table.setHorizontalHeaderLabels(header_labels)

                    for i, holding in enumerate(holdings):
                        self.holdings_table.setItem(i, 0, QTableWidgetItem(str(holding['stock_id'])))
                        self.holdings_table.setItem(i, 1, QTableWidgetItem(holding['stock_name']))
                        self.holdings_table.setItem(i, 2, QTableWidgetItem(str(holding['quantity'])))

                    # 设置表格内容不可编辑
                    self.holdings_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                    self.holdings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                    self.holdings_table.horizontalHeader().setStretchLastSection(True)
                    self.holdings_table.horizontalHeader().setFixedHeight(50)

                    # 启用水平和垂直滚动
                    self.holdings_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                    self.holdings_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

                    self.view_fund_layout.addWidget(self.holdings_table)

                else:
                    QMessageBox.critical(self, "错误", f"获取持股列表失败: {response.json().get('message', '未知错误')}")
            except requests.exceptions.HTTPError as http_err:
                QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
            except requests.exceptions.RequestException as req_err:
                QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"获取持股列表失败: {e}")

            self.back_button = QPushButton("返回基金列表", self)
            self.back_button.clicked.connect(self.show_view_fund)
            self.view_fund_layout.addWidget(self.back_button)

    def show_manager_funds(self, row, column):
        if column == 4:  # Manager 列
            manager_username = self.fund_table.item(row, column).text()
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

                    self.view_fund_layout.addWidget(self.fund_table)

                else:
                    QMessageBox.critical(self, "错误", f"获取基金列表失败: {response.json().get('message', '未知错误')}")
            except requests.exceptions.HTTPError as http_err:
                QMessageBox.critical(self, "错误", f"HTTP错误: {http_err}")
            except requests.exceptions.RequestException as req_err:
                QMessageBox.critical(self, "错误", f"请求错误: {req_err}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"获取基金列表失败: {e}")

            self.back_button = QPushButton("返回基金管理", self)
            self.back_button.clicked.connect(self.initUI)
            self.view_fund_layout.addWidget(self.back_button)
            
    def show_manage_fund(self):
        self.clear_content()
        # 管理基金界面的实现，仅显示当前基金经理管理的基金
        try:
            response = self.session.get(f"{BASE_URL}/funds/manager/{self.parent.username}")
            response.raise_for_status()
            funds = response.json()
            self.display_funds(funds)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"获取基金列表失败: {e}")     
            
    def show_user_funds(self):
        self.clear_content()
        # 查看用户持有的基金界面的实现，仅显示当前用户持有的基金
        try:
            response = self.session.get(f"{BASE_URL}/user/{self.parent.username}/funds")
            response.raise_for_status()
            funds = response.json()
            self.display_funds(funds)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"获取基金列表失败: {e}")
            
    def show_view_fund(self):
        self.clear_content()
        # 查看所有基金界面的实现
        try:
            response = self.session.get(f"{BASE_URL}/funds")
            response.raise_for_status()
            funds = response.json()
            self.display_funds(funds)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"获取基金列表失败: {e}")
    def display_funds(self, funds):
        self.view_fund_layout = QVBoxLayout()
        self.layout.addLayout(self.view_fund_layout)

        self.view_fund_layout.addWidget(QLabel("基金列表", self))

        # 添加搜索栏
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("搜索基金...")
        self.search_bar.textChanged.connect(self.filter_funds)
        self.view_fund_layout.addWidget(self.search_bar)

        self.fund_table = QTableWidget()
        self.fund_table.setRowCount(len(funds))
        self.fund_table.setColumnCount(len(fields) + 1)  # 加上持仓金额列

        # 设置表头标签
        header_labels = ["ID"] + list(fields.keys()) + ["持仓金额"]
        self.fund_table.setHorizontalHeaderLabels(header_labels)

        headers = ['id'] + list(fields.values())

        for i, fund in enumerate(funds):
            for j, header in enumerate(headers):
                if header == 'manager':
                    value = fund['manager']['username']
                elif header == 'total_holdings_value':
                    value = fund.get('total_holdings_value', 0.0)
                else:
                    value = fund.get(header, "")
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
        self.fund_table.cellDoubleClicked.connect(self.show_fund_holdings)

        self.view_fund_layout.addWidget(self.fund_table)

        # 添加统计信息显示区域
        self.stats_label = QLabel(self)
        self.view_fund_layout.addWidget(self.stats_label)
        self.update_stats(funds)

        self.back_button = QPushButton("返回基金管理", self)
        self.back_button.clicked.connect(self.initUI)
        self.view_fund_layout.addWidget(self.back_button)

    def filter_funds(self):
        search_text = self.search_bar.text().lower()
        for row in range(self.fund_table.rowCount()):
            fund_name = self.fund_table.item(row, 1).text().lower()
            if search_text in fund_name:
                self.fund_table.setRowHidden(row, False)
            else:
                self.fund_table.setRowHidden(row, True)

    def update_stats(self, funds):
        total_funds = len(funds)
        total_value = sum(fund.get('total_holdings_value', 0.0) for fund in funds)
        self.stats_label.setText(f"总基金数量: {total_funds}, 总持仓金额: {total_value:.2f}")
    # def display_funds(self, funds):
    #     self.view_fund_layout = QVBoxLayout()
    #     self.layout.addLayout(self.view_fund_layout)

    #     self.view_fund_layout.addWidget(QLabel("基金列表", self))

    #     self.fund_table = QTableWidget()
    #     self.fund_table.setRowCount(len(funds))
    #     self.fund_table.setColumnCount(len(fields) + 1)  # 加上持仓金额列

    #     # 设置表头标签
    #     header_labels = ["ID"] + list(fields.keys()) + ["持仓金额"]
    #     self.fund_table.setHorizontalHeaderLabels(header_labels)

    #     headers = ['id'] + list(fields.values())

    #     for i, fund in enumerate(funds):
    #         for j, header in enumerate(headers):
    #             if header == 'manager':
    #                 value = fund['manager']['username']
    #             elif header == 'total_holdings_value':
    #                 value = fund.get('total_holdings_value', 0.0)
    #             # elif header == 'inception_date' and value:
    #             #     value = value[:10]  # 只取日期部分
    #             else:
    #                 value = fund.get(header, "")
    #             self.fund_table.setItem(i, j, QTableWidgetItem(str(value)))

    #     # 设置表格内容不可编辑
    #     self.fund_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    #     self.fund_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #     self.fund_table.horizontalHeader().setStretchLastSection(True)
    #     self.fund_table.horizontalHeader().setFixedHeight(50)

    #     # 启用水平和垂直滚动
    #     self.fund_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    #     self.fund_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    #     self.fund_table.cellDoubleClicked.connect(self.show_manager_funds)
    #     self.fund_table.cellDoubleClicked.connect(self.show_fund_holdings)

    #     self.view_fund_layout.addWidget(self.fund_table)

    #     self.back_button = QPushButton("返回基金管理", self)
    #     self.back_button.clicked.connect(self.initUI)
    #     self.view_fund_layout.addWidget(self.back_button)

            
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

