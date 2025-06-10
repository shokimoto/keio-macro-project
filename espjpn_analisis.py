# 必要なライブラリのインポート
import pandas as pd
import matplotlib.pyplot as plt

# データ取得関数（仮）
def get_macro_data(country_code, start, end):
    series_ids = {
    'JP': {
        'gdp': 'JPNRGDPEXP',
        'consumption': 'JPNPFCEADSMEI',
        'investment': 'JPNGFCFADSMEI',
    },
    'ES': {
        'gdp': 'ESPNRGDPEXP',
        'consumption': 'ESPPFCEADSMEI',
        'investment': 'ESPGFCFADSMEI',
    }
}

    # 必要に応じてAPIやデータ読み込み処理を書く
    pass  # 仮置き

# トレンド・循環成分の分解関数（HPフィルターなど想定）
def process_cycle_data(data):
    # 'gdp', 'consumption', 'investment' を含む辞書で返す
    pass  # 仮置き

# 統計計算関数
def calculate_statistics(cycle_data):
    stats = {
        'gdp': [cycle_data['gdp'].std() * 100, cycle_data['gdp'].autocorr(), cycle_data['gdp'].corr(cycle_data['gdp'])],
        'consumption': [cycle_data['consumption'].std() * 100, cycle_data['consumption'].autocorr(), cycle_data['consumption'].corr(cycle_data['gdp'])],
        'investment': [cycle_data['investment'].std() * 100, cycle_data['investment'].autocorr(), cycle_data['investment'].corr(cycle_data['gdp'])],
    }
    return (pd.DataFrame(stats).T
            .rename(columns={0: 'std_dev', 1: 'autocorr', 2: 'corr_with_gdp'}))

# 比較表作成関数
def create_statistics_table(sp_stats, jp_stats):
    sp_std, sp_auto, sp_corr = sp_stats['std_dev'], sp_stats['autocorr'], sp_stats['corr_with_gdp']
    jp_std, jp_auto, jp_corr = jp_stats['std_dev'], jp_stats['autocorr'], jp_stats['corr_with_gdp']

    stats_data = {
        ('Volatility (%)', 'Spain'): sp_std,
        ('Volatility (%)', 'Japan'): jp_std,
        ('Persistence', 'Spain'): sp_auto,
        ('Persistence', 'Japan'): jp_auto,
        ('Corr. with GDP', 'Spain'): sp_corr,
        ('Corr. with GDP', 'Japan'): jp_corr
    }
    columns = pd.MultiIndex.from_tuples(stats_data.keys())
    stats_df = pd.DataFrame(stats_data, index=['gdp', 'consumption', 'investment'])
    return stats_df

# 循環成分の標準偏差・相関の比較
def compare_cycle_statistics(sp_cycles, jp_cycles):
    vars = set(sp_cycles.keys()) & set(jp_cycles.keys())
    rows = []
    for var in vars:
        sp = sp_cycles[var].dropna()
        jp = jp_cycles[var].dropna()
        df = pd.concat([sp, jp], axis=1, join='inner')
        rows.append({
            'variable': var,
            'std_spain (%)': sp.std() * 100,
            'std_japan (%)': jp.std() * 100,
            'corr_spain_japan': df.iloc[:, 0].corr(df.iloc[:, 1])
        })
    return pd.DataFrame(rows).set_index('variable')

# 循環成分プロット関数
def plot_cycle_comparison(country1, cycles1, country2, cycles2):
    variables = ['gdp', 'consumption', 'investment']
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for i, var in enumerate(variables):
        ax = axes[i]
        if var in cycles1 and var in cycles2:
            cycles1[var].plot(ax=ax, label=country1, linewidth=1.5)
            cycles2[var].plot(ax=ax, label=country2, linewidth=1.5)
            ax.axhline(0, color='black', linestyle='-', alpha=0.3)
            ax.set_title(f"{var.capitalize()} Cycle: {country1} vs {country2}")
            ax.legend()
            ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{country1.lower()}_{country2.lower()}_cycle_comparison.png", dpi=300, bbox_inches='tight')
    plt.show()

# トレンド＋循環の描画関数（仮）
def plot_trends_and_cycles(country, raw_data, cycles, trends):
    pass  # 実装済みを仮定

# 分析実行関数
def analyze_business_cycles_spain_japan():
    print("Fetching Spain macroeconomic data...")
    sp_data = get_macro_data('ES', start_date, end_date)
    print("Spain data preview:", sp_data)

    print("Fetching Japan macroeconomic data...")
    jp_data = get_macro_data('JP', start_date, end_date)

    print("Processing Spain data...")
    sp_cycles, sp_trends = process_cycle_data(sp_data)

    print("Processing Japan data...")
    jp_cycles, jp_trends = process_cycle_data(jp_data)

    print("Calculating statistics...")
    sp_stats = calculate_statistics(sp_cycles)
    jp_stats = calculate_statistics(jp_cycles)

    print("Creating comparison table...")
    stats_table = create_statistics_table(sp_stats, jp_stats)
    print("\nBusiness Cycle Statistics:\n")
    print(stats_table.round(3))

    print("Plotting trends and cycles for Spain...")
    plot_trends_and_cycles("Spain", sp_data, sp_cycles, sp_trends)

    print("Plotting trends and cycles for Japan...")
    plot_trends_and_cycles("Japan", jp_data, jp_cycles, jp_trends)

    print("\nSpain vs Japan: Cycle Comparison Table")
    comp_df = compare_cycle_statistics(sp_cycles, jp_cycles)
    print(comp_df.round(3))

    print("\nPlotting Spain vs Japan cycle comparison...")
    plot_cycle_comparison("Spain", sp_cycles, "Japan", jp_cycles)

# 日付の指定（適宜設定）
start_date = '1995-01-01'
end_date = '2025-01-01'

# スクリプトが直接実行されたときのみ分析を実行
if __name__ == "__main__":
    analyze_business_cycles_spain_japan()

