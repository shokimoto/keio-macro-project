import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from datetime import datetime
from statsmodels.tsa.stattools import acf
from matplotlib.gridspec import GridSpec

plt.style.use('ggplot')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
                                                    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'])

start_date = '1994-01-01'
end_date = '2025-01-01'

def get_macro_data(country_code, start_date, end_date):
    """
    Fetch macroeconomic data for a specific country from FRED
    
    Parameters:
    country_code (str): 'US', 'JP', or 'ES'
    
    Returns:
    dict: Dictionary containing DataFrames for GDP, consumption, and investment
    """
    data = {}
    series_ids = {
        'US': {
            'gdp': 'GDPC1',              # Real GDP (Quarterly)
            'consumption': 'PCECC96',     # Real Personal Consumption Expenditures
            'investment': 'GPDIC1',       # Real Gross Private Domestic Investment
        },
        'JP': {
            'gdp': 'JPNRGDPEXP',         # Japan Real GDP
            'consumption': 'JPNPFCEADSMEI', # Japan Private Final Consumption Expenditure
            'investment': 'JPNGFCFADSMEI', # Japan Gross Fixed Capital Formation
        },
        'ES': {
            # 以下は例示、実際にFREDにあるスペインのマクロ指標IDに置き換えてください
            'gdp': 'CLVMNACNSAB1GQES',        # Spain Real GDP (例)
            'consumption': 'PCES',             # Spain Private Consumption (仮のID)
            'investment': 'GFCEES',            # Spain Gross Fixed Capital Formation (仮のID)
        }
    }

    for var, series_id in series_ids.get(country_code, {}).items():
        try:
            data[var] = web.DataReader(series_id, 'fred', start_date, end_date)
        except Exception as e:
            print(f"Error fetching {var} data for {country_code}: {e}")
            data[var] = None
    return data

def process_cycle_data(data, lamb=1600):
    cycles = {}
    trends = {}
    for var, df in data.items():
        if df is not None and not df.empty:
            series = df.squeeze()
            log_data = np.log(series)
            cycle, trend = sm.tsa.filters.hpfilter(log_data, lamb=lamb)
            cycles[var] = cycle
            trends[var] = trend
    return cycles, trends

def calculate_statistics(cycles):
    cycle_df = pd.DataFrame({var: cycle for var, cycle in cycles.items()})
    std_dev = cycle_df.std() * 100
    autocorr = pd.Series({var: acf(cycle_df[var].dropna(), nlags=1)[1] for var in cycle_df.columns})
    corr_with_gdp = cycle_df.corr()['gdp']
    return std_dev, autocorr, corr_with_gdp

def plot_trends_and_cycles(country, raw_data, cycles, trends):
    variables = ['gdp', 'consumption', 'investment']
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig)
    for i, var in enumerate(variables):
        if var in raw_data and raw_data[var] is not None:
            ax1 = fig.add_subplot(gs[i, 0])
            log_data = np.log(raw_data[var])
            log_data.plot(ax=ax1, label=f"Log {var.capitalize()}")
            trends[var].plot(ax=ax1, label="Trend", linewidth=2, color='red')
            ax1.set_title(f"{var.capitalize()} and Trend for {country}")
            ax1.legend()
            
            ax2 = fig.add_subplot(gs[i, 1])
            cycles[var].plot(ax=ax2, label="Cyclical Component", color='green')
            ax2.set_title(f"{var.capitalize()} Cycle for {country}")
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax2.legend()
    plt.tight_layout()
    plt.savefig(f"{country.lower().replace(' ', '_')}_trends_and_cycles.png", dpi=300, bbox_inches='tight')
    plt.show()

# 以下の関数は共通なのでそのまま
def create_statistics_table(spain_stats, us_stats):
    sp_std, sp_auto, sp_corr = spain_stats
    us_std, us_auto, us_corr = us_stats
    
    stats_data = {
        ('Volatility (%)', 'Spain'): sp_std,
        ('Volatility (%)', 'US'): us_std,
        ('Persistence', 'Spain'): sp_auto,
        ('Persistence', 'US'): us_auto,
        ('Corr. with GDP', 'Spain'): sp_corr,
        ('Corr. with GDP', 'US'): us_corr
    }
    
    columns = pd.MultiIndex.from_tuples(stats_data.keys())
    stats_df = pd.DataFrame(stats_data, index=['gdp', 'consumption', 'investment'])
    return stats_df

def analyze_business_cycles():
    print("Fetching Spain macroeconomic data...")
    sp_data = get_macro_data('ES', start_date, end_date)
    
    print("Fetching US macroeconomic data...")
    us_data = get_macro_data('US', start_date, end_date)
    
    print("Processing Spain data...")
    sp_cycles, sp_trends = process_cycle_data(sp_data)
    
    print("Processing US data...")
    us_cycles, us_trends = process_cycle_data(us_data)
    
    print("Calculating statistics...")
    sp_stats = calculate_statistics(sp_cycles)
    us_stats = calculate_statistics(us_cycles)
    
    print("Creating comparison table...")
    stats_table = create_statistics_table(sp_stats, us_stats)
    print("\nBusiness Cycle Statistics:\n")
    print(stats_table.round(3))
    
    print("\nPlotting trends and cycles for Spain...")
    plot_trends_and_cycles("Spain", sp_data, sp_cycles, sp_trends)
    
    print("Plotting trends and cycles for US...")
    plot_trends_and_cycles("United States", us_data, us_cycles, us_trends)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    variables = ['gdp', 'consumption', 'investment']
    for i, var in enumerate(variables):
        if var in sp_cycles and var in us_cycles:
            sp_cycles[var].plot(ax=axes[i], label=f"Spain {var.capitalize()}", linewidth=1.5)
            us_cycles[var].plot(ax=axes[i], label=f"US {var.capitalize()}", linewidth=1.5)
            axes[i].set_title(f"{var.capitalize()} Cycle: Spain vs US")
            axes[i].axhline(y=0, color='black', linestyle='-', alpha=0.3)
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("spain_us_cycle_comparison.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    analyze_business_cycles()
