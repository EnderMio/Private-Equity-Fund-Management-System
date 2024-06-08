from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem
import requests
from config import BASE_URL

class StockManagement(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Stock Management", self))

        self.add_stock_button = QPushButton("Add Stock", self)
        self.add_stock_button.clicked.connect(self.add_stock)
        layout.addWidget(self.add_stock_button)

        self.update_stock_button = QPushButton("Update Stock", self)
        self.update_stock_button.clicked.connect(self.update_stock)
        layout.addWidget(self.update_stock_button)

        self.delete_stock_button = QPushButton("Delete Stock", self)
        self.delete_stock_button.clicked.connect(self.delete_stock)
        layout.addWidget(self.delete_stock_button)

        self.view_stocks_button = QPushButton("View Stock List", self)
        self.view_stocks_button.clicked.connect(self.view_stocks)
        layout.addWidget(self.view_stocks_button)

    def add_stock(self):
        self.clear_layout()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Add Stock", self))

        layout.addWidget(QLabel("Stock Name"))
        self.stock_name_entry = QLineEdit(self)
        layout.addWidget(self.stock_name_entry)

        layout.addWidget(QLabel("Stock Symbol"))
        self.stock_symbol_entry = QLineEdit(self)
        layout.addWidget(self.stock_symbol_entry)

        layout.addWidget(QLabel("Stock Price"))
        self.stock_price_entry = QLineEdit(self)
        layout.addWidget(self.stock_price_entry)

        self.add_stock_submit_button = QPushButton("Add Stock", self)
        self.add_stock_submit_button.clicked.connect(self.handle_add_stock)
        layout.addWidget(self.add_stock_submit_button)

        self.back_button = QPushButton("Back to Stock Management", self)
        self.back_button.clicked.connect(self.initUI)
        layout.addWidget(self.back_button)

    def handle_add_stock(self):
        stock_name = self.stock_name_entry.text()
        stock_symbol = self.stock_symbol_entry.text()
        stock_price = self.stock_price_entry.text()

        payload = {
            "name": stock_name,
            "symbol": stock_symbol,
            "price": stock_price
        }

        try:
            response = requests.post(f"{BASE_URL}/stocks", json=payload)

            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Stock added successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to add stock: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add stock: {e}")

    def update_stock(self):
        self.clear_layout()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Update Stock", self))

        layout.addWidget(QLabel("Stock ID"))
        self.stock_id_entry = QLineEdit(self)
        layout.addWidget(self.stock_id_entry)

        layout.addWidget(QLabel("New Stock Name"))
        self.stock_name_entry = QLineEdit(self)
        layout.addWidget(self.stock_name_entry)

        layout.addWidget(QLabel("New Stock Symbol"))
        self.stock_symbol_entry = QLineEdit(self)
        layout.addWidget(self.stock_symbol_entry)

        layout.addWidget(QLabel("New Stock Price"))
        self.stock_price_entry = QLineEdit(self)
        layout.addWidget(self.stock_price_entry)

        self.update_stock_submit_button = QPushButton("Update Stock", self)
        self.update_stock_submit_button.clicked.connect(self.handle_update_stock)
        layout.addWidget(self.update_stock_submit_button)

        self.back_button = QPushButton("Back to Stock Management", self)
        self.back_button.clicked.connect(self.initUI)
        layout.addWidget(self.back_button)

    def handle_update_stock(self):
        stock_id = self.stock_id_entry.text()
        stock_name = self.stock_name_entry.text()
        stock_symbol = self.stock_symbol_entry.text()
        stock_price = self.stock_price_entry.text()

        payload = {
            "name": stock_name,
            "symbol": stock_symbol,
            "price": stock_price
        }

        try:
            response = requests.put(f"{BASE_URL}/stocks/{stock_id}", json=payload)

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Stock updated successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to update stock: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update stock: {e}")

    def delete_stock(self):
        self.clear_layout()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Delete Stock", self))

        layout.addWidget(QLabel("Stock ID"))
        self.stock_id_entry = QLineEdit(self)
        layout.addWidget(self.stock_id_entry)

        self.delete_stock_submit_button = QPushButton("Delete Stock", self)
        self.delete_stock_submit_button.clicked.connect(self.handle_delete_stock)
        layout.addWidget(self.delete_stock_submit_button)

        self.back_button = QPushButton("Back to Stock Management", self)
        self.back_button.clicked.connect(self.initUI)
        layout.addWidget(self.back_button)

    def handle_delete_stock(self):
        stock_id = self.stock_id_entry.text()

        try:
            response = requests.delete(f"{BASE_URL}/stocks/{stock_id}")

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Stock deleted successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete stock: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete stock: {e}")

    def view_stocks(self):
        self.clear_layout()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Stock List", self))

        try:
            response = requests.get(f"{BASE_URL}/stocks")

            if response.status_code == 200:
                stocks = response.json()

                self.stock_table = QTableWidget()
                self.stock_table.setRowCount(len(stocks))
                self.stock_table.setColumnCount(4)
                self.stock_table.setHorizontalHeaderLabels(["ID", "Name", "Symbol", "Price"])
                for i, stock in enumerate(stocks):
                    self.stock_table.setItem(i, 0, QTableWidgetItem(str(stock["id"])))
                    self.stock_table.setItem(i, 1, QTableWidgetItem(stock["name"]))
                    self.stock_table.setItem(i, 2, QTableWidgetItem(stock["symbol"]))
                    self.stock_table.setItem(i, 3, QTableWidgetItem(str(stock["price"])))

                layout.addWidget(self.stock_table)
            else:
                QMessageBox.critical(self, "Error", f"Failed to fetch stocks: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch stocks: {e}")

        self.back_button = QPushButton("Back to Stock Management", self)
        self.back_button.clicked.connect(self.initUI)
        layout.addWidget(self.back_button)

    def clear_layout(self):
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
