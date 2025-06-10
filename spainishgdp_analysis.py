import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter

# ① CSVファイル読み込み
df = pd.read_csv('spain_gdp.csv')
print(df.head())     # 最初の5行を表示
print(df.columns)    # 列名一覧を表示

# 日付列（observation_date列）を日時型に変換し、インデックスに設定
df['observation_date'] = pd.to_datetime(df['observation_date'])
df.set_index('observation_date', inplace=True)

# ② 対数変換（B列がGDP値）
df_log = np.log(df['GDP'])

# ③ HPフィルターでトレンドとサイクルに分解（lamb=1600は四半期データの標準）
cycle, trend = hpfilter(df_log, lamb=1600)

# ④ グラフ表示
plt.figure(figsize=(12,6))
plt.plot(df_log.index, df_log, label='Log GDP')
plt.plot(trend.index, trend, label='Trend')
plt.plot(cycle.index, cycle, label='Cycle')
plt.legend()
plt.title('HP Filter Decomposition of Spain GDP')
plt.show()
