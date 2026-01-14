import pandas as pd
df = pd.read_feather("../user_data/data/binance/BTC_USDT-5m.feather")
print(df.head())
print(df.tail())