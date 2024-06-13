from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit, QScrollArea, QFormLayout, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
import requests
from config import BASE_URL
from .stock_fields import create_stock_form_layout, stock_fields
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import requests
import datetime
import yfinance as yf

class StockManagement(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        print("正在初始化股票管理...")  # 调试信息
        self.session = parent.session  # 使用父组件的会话对象
        self.parent = parent
        self.user_role = parent.user_role  # 获取用户角色
        self.scroll_area = None  # 初始化 scroll_area
        self.layout = QVBoxLayout()  # 初始化主布局
        self.setLayout(self.layout)
        self.initUI()
        print("股票管理初始化成功。")  # 调试信息

    def initUI(self):
        self.clear_content()

        if self.user_role == 'admin':
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
        self.back_button.clicked.connect(self.initUI)
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
        self.back_button.clicked.connect(self.initUI)
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
        self.back_button.clicked.connect(self.initUI)
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

                self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                # 设置表头宽度和列宽度
                self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.stock_table.horizontalHeader().setStretchLastSection(True)

                # 设置表头行的高度
                self.stock_table.horizontalHeader().setFixedHeight(50)

                self.stock_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.stock_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                self.stock_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

                self.stock_table.cellDoubleClicked.connect(self.show_stock_details)

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
        self.back_button.clicked.connect(self.initUI)
        self.view_stock_layout.addWidget(self.back_button)

    def show_stock_details(self, row, column):
        if column == 1:  # 假设股票名称列为第2列，股票代码列为第1列
            stock_code = self.stock_table.item(row, 2).text()  # 获取股票代码
            stock_name = self.stock_table.item(row, 1).text()
            self.clear_content()
            self.view_stock_layout = QVBoxLayout()
            self.layout.addLayout(self.view_stock_layout)

            self.view_stock_layout.addWidget(QLabel(f"{stock_name} ({stock_code}) 的交易数据与KDJ图表", self))

            try:
                # 爬取交易数据
                stock_data = self.fetch_stock_data(stock_code)
                if stock_data.empty:
                    raise ValueError("未能获取到交易数据")

                # 计算KDJ指标
                stock_data = self.calculate_kdj(stock_data)

                # 绘制交易数据与KDJ图表
                self.plot_stock_data(stock_data, stock_code)

                # 根据J值判断超买超卖并显示仓位管理建议
                self.display_position_management(stock_data)

            except Exception as e:
                QMessageBox.critical(self, "错误", f"获取股票数据失败: {e}")

            self.back_button = QPushButton("返回股票列表", self)
            self.back_button.clicked.connect(self.show_view_stock)
            self.view_stock_layout.addWidget(self.back_button)

    def fetch_stock_data(self, stock_code):
        try:
            # 使用yfinance获取股票的历史交易数据
            print(f"正在获取 {stock_code} 的历史交易数据...")  # 调试信息
            stock = yf.Ticker(stock_code)
            hist = stock.history(period="1y")  # 获取过去一年的数据

            if hist.empty:
                print(f"未能获取到 {stock_code} 的交易数据。")  # 调试信息
                return pd.DataFrame()

            hist.reset_index(inplace=True)
            hist.rename(columns={"Date": "date", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}, inplace=True)

            print(f"成功获取 {stock_code} 的交易数据：")  # 调试信息
            print(hist.head())  # 显示前几行数据以验证成功获取

            return hist
        except Exception as e:
            print(f"获取 {stock_code} 的交易数据时发生错误：{e}")  # 调试信息
            return pd.DataFrame()

    def calculate_kdj(self, df):
        df.columns = [col.lower() for col in df.columns]  # 统一将所有列名转换为小写
        low_list = df['low'].rolling(9, min_periods=9).min()
        low_list.fillna(value=df['low'].expanding().min(), inplace=True)
        high_list = df['high'].rolling(9, min_periods=9).max()
        high_list.fillna(value=df['high'].expanding().max(), inplace=True)
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100

        df['k'] = pd.DataFrame(rsv).ewm(com=2).mean()
        df['d'] = df['k'].ewm(com=2).mean()
        df['j'] = 3 * df['k'] - 2 * df['d']
        return df

    def plot_stock_data(self, df, stock_code):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # 绘制收盘价
        ax1.plot(df['date'], df['close'], label='Close Price')
        ax1.set_title(f'{stock_code} Close Price - Last Year')
        ax1.set_ylabel('Price')
        ax1.legend()

        # 绘制KDJ指标
        ax2.plot(df['date'], df['k'], label='K')
        ax2.plot(df['date'], df['d'], label='D')
        ax2.plot(df['date'], df['j'], label='J')
        ax2.set_ylabel('Value')
        ax2.legend()
        
        fig.subplots_adjust(hspace=0.4)

        canvas = FigureCanvas(fig)
        self.view_stock_layout.addWidget(canvas)

    def display_position_management(self, df):
        latest_j = df['j'].iloc[-1]
        advice = "持仓建议："
        if latest_j > 80:
            advice += "超买，建议减仓。"
        elif latest_j < 20:
            advice += "超卖，建议加仓。"
        else:
            advice += "正常，建议持仓不变。"

        self.view_stock_layout.addWidget(QLabel(advice, self))

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


