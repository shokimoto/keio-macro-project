import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from datetime import datetime
from statsmodels.tsa.stattools import acf, ccf
from matplotlib.gridspec import GridSpec

# Set the style for all plots
plt.style.use('ggplot')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
                                                    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'])

# Set the start and end dates for the data
start_date = '1994-01-01'  # Starting from 1980 for better data availability for Japan
end_date = '2025-01-01'
def get_macro_data(country_code, start_date, end_date):

    """
    Fetch macroeconomic data for a specific country from FRED
    
    Parameters:
    country_code (str): 'JP' for United States, 'JP' for Japan
    
    Returns:
    dict: Dictionary containing DataFrames for GDP, consumption, and investment
    """
    data = get_macro_data('JP', '1994-01-01', '2025-01-01')
    
    # Dictionary of FRED series IDs for each country and variable
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
        }
    }
    
    # Fetch data for each variable
    for var, series_id in series_ids[country_code].items():
        try:
            data[var] = web.DataReader(series_id, 'fred', start_date, end_date)
        except Exception as e:
            print(f"Error fetching {var} data for {country_code}: {e}")
            data[var] = None
    
    return data