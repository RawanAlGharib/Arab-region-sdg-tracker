import wbgapi as wb
import pandas as pd
import sqlite3

print("⏳ Step 1: Extracting data from the World Bank API...")

# Define our 3 Core SDG Indicators
indicator_map = {
    'SL.TLF.CACT.FE.ZS': 'Female Labor Force Participation (%)',
    'NY.GDP.PCAP.KD.ZG': 'GDP per Capita Growth (%)',
    'IT.NET.USER.ZS': 'Internet Penetration (%)'
}
indicator_codes = list(indicator_map.keys())

# Pull data for the last decade (2013-2023)
raw_data = wb.data.DataFrame(indicator_codes, time=range(2013, 2024), numericTimeKeys=True).reset_index()

# Pull Country Metadata (Regions and Income Levels)
countries = wb.economy.DataFrame().reset_index()
countries = countries[['id', 'name', 'region', 'incomeLevel']].dropna()

print("🧹 Step 2: Cleaning and structuring the tables...")

# TABLE 1: dim_countries
dim_countries = countries.rename(columns={
    'id': 'country_code', 
    'name': 'country_name', 
    'region': 'region_code', 
    'incomeLevel': 'income_group'
})

# TABLE 2: dim_indicators
dim_indicators = pd.DataFrame(list(indicator_map.items()), columns=['indicator_code', 'indicator_name'])

# TABLE 3: fact_sdg_data (Unpivoting the data to make it SQL-ready)
# wbgapi returns a column for 'economy' and 'series'. We melt the year columns into rows.
fact_sdg_data = pd.melt(
    raw_data, 
    id_vars=['economy', 'series'], 
    var_name='year', 
    value_name='indicator_value'
)
fact_sdg_data = fact_sdg_data.rename(columns={'economy': 'country_code', 'series': 'indicator_code'})
fact_sdg_data = fact_sdg_data.dropna(subset=['indicator_value']) # Remove empty rows

print("💾 Step 3: Loading data into SQLite Database...")

# Create the database file locally
conn = sqlite3.connect('sdg_database.db')

# Push the dataframes into the database as separate tables
dim_countries.to_sql('dim_countries', conn, if_exists='replace', index=False)
dim_indicators.to_sql('dim_indicators', conn, if_exists='replace', index=False)
fact_sdg_data.to_sql('fact_sdg_data', conn, if_exists='replace', index=False)

conn.close()

print("✅ Success! 'sdg_database.db' has been created in your folder.")