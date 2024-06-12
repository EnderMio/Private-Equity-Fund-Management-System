from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit

fields = {
    "基金名称": "name",
    "基金描述": "description",
    "基金金额": "amount",
    "基金经理": "manager",
    "基金类型": "type",
    "持仓金额": "total_holdings_value",
    "市盈率": "pe_ratio",
    "市净率": "pb_ratio",
    "总市值": "total_market_value",
    "成立日期": "inception_date",
    "费用率": "expense_ratio",
    "净值": "nav",
    "风险等级": "risk_level",
    "最近一年回报率": "return_rate_1y",
    "最近三年回报率": "return_rate_3y",
    "最近五年回报率": "return_rate_5y",
}

def create_form_layout(parent):
    grid_layout = QGridLayout()
    entries = {}
    
    for i, (label_text, field_name) in enumerate(fields.items()):
        grid_layout.addWidget(QLabel(label_text, parent), i // 2, (i % 2) * 2)
        entry = QLineEdit(parent)
        grid_layout.addWidget(entry, i // 2, (i % 2) * 2 + 1)
        entries[field_name] = entry

    return grid_layout, entries
