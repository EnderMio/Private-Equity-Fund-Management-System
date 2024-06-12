import yfinance as yf
import matplotlib.pyplot as plt

# 获取苹果公司股票数据
ticker = 'AAPL'
apple_stock = yf.Ticker(ticker)

# 获取历史市场数据
hist = apple_stock.history(period="1y")  # 过去一年的数据

# 打印股票基本信息
print(apple_stock.info)

# 打印历史数据
print(hist)

# 绘制收盘价图表
plt.figure(figsize=(10, 6))
plt.plot(hist.index, hist['Close'], label='Close Price')
plt.title('Apple Stock Close Price - Last Year')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.grid(True)
plt.show()