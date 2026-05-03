import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 使用者輸入

ticker = input("請輸入股票代碼，例如 2330.TW： ")
start = input("請輸入起始日期 (YYYY-MM-DD)： ")
end = input("請輸入結束日期 (YYYY-MM-DD)： ")

# 下載股價資料
data = yf.download(ticker, start=start, end=end)

# 計算移動平均線 MA
data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA60"] = data["Close"].rolling(window=60).mean()

# 計算布林通道
data["Middle"] = data["MA20"]
data["STD20"] = data["Close"].rolling(window=20).std()
data["Upper"] = data["Middle"] + 2 * data["STD20"]
data["Lower"] = data["Middle"] - 2 * data["STD20"]

# 計算 RSI
delta = data["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
period = 14
avg_gain = gain.rolling(window=period).mean()
avg_loss = loss.rolling(window=period).mean()
RS = avg_gain / avg_loss
data["RSI"] = 100 - (100 / (1 + RS))

print(data.tail())

# 圖表 1：價格 + MA
plt.figure(figsize=(12,5))
plt.plot(data["Close"], label="Close")
plt.plot(data["MA20"], label="MA20")
plt.plot(data["MA60"], label="MA60")
plt.title("MA")
plt.legend()
plt.grid(True)
plt.show()

# 圖表 2：布林通道
plt.figure(figsize=(12,5))
plt.plot(data["Close"], label="Close")
plt.plot(data["Upper"], label="Upper Band")
plt.plot(data["Middle"], label="Middle Band")
plt.plot(data["Lower"], label="Lower Band")
plt.title("Bollinger Bands")
plt.legend()
plt.grid(True)
plt.show()

# 圖表 3：RSI
plt.figure(figsize=(12,3))
plt.plot(data["RSI"], label="RSI")
plt.axhline(70, linestyle="--")
plt.axhline(30, linestyle="--")
plt.title("RSI")
plt.legend()
plt.grid(True)
plt.show()
