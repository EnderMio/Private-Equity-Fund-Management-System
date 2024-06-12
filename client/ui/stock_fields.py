from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit

stock_fields = {
    "股票名称": "name",
    "股票符号": "symbol",
    "股票价格": "price",
    "股票市值": "market_cap",
    "市盈率": "pe_ratio",
    "市净率": "pb_ratio",
    "股息率": "dividend_yield",
    "流通股数": "shares_outstanding",
    "行业": "industry",
    "上市日期": "ipo_date"
}

def create_stock_form_layout(parent):
    grid_layout = QGridLayout()
    entries = {}
    
    for i, (label_text, field_name) in enumerate(stock_fields.items()):
        grid_layout.addWidget(QLabel(label_text, parent), i // 2, (i % 2) * 2)
        entry = QLineEdit(parent)
        grid_layout.addWidget(entry, i // 2, (i % 2) * 2 + 1)
        entries[field_name] = entry

    return grid_layout, entries
