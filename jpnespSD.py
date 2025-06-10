import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter

# データ読み込み関数（国ごとに列名を指定）
def load_and_prepare(file_path, date_col, gdp_col):
    df = pd.read_csv(file_path)
    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)
    df = df['1995-01-01':'2025-01-01']
    return df[gdp_col]

# HPフィルターを使ってトレンド・循環成分を抽出
def extract_cycle(series, lamb=1600):
    cycle, trend = hpfilter(series, lamb=lamb)
    return cycle

# ファイルパスと列名の設定
spain_file = 'spain_gdp.csv'
japan_file = 'jpn_gdp.csv'

# スペインと日本のGDPを読み込み（observation_date列を使用）
spain_gdp = load_and_prepare(spain_file, date_col='observation_date', gdp_col='CLVMNACSCAB1GQES')
japan_gdp = load_and_prepare(japan_file, date_col='observation_date', gdp_col='JPNRGDPEXP')

# HPフィルターで循環成分を抽出
spain_cycle = extract_cycle(spain_gdp)
japan_cycle = extract_cycle(japan_gdp)

# 標準偏差の計算
spain_std = spain_cycle.std() * 100
japan_std = japan_cycle.std() * 100

print("循環変動成分の標準偏差（%）:")
print(f"スペイン: {spain_std:.2f}%")
print(f"日本: {japan_std:.2f}%")

# オプション：グラフで比較
plt.figure(figsize=(10, 5))
spain_cycle.plot(label='Spain', linewidth=2)
japan_cycle.plot(label='Japan', linewidth=2)
plt.axhline(0, color='black', linestyle='--', alpha=0.6)
plt.title('the cyclical component of GDP: Spain vs Japan')
plt.ylabel('Cycle')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("gdp_cycle_comparison.png", dpi=300)
plt.show()
