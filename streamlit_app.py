import streamlit as st
import pandas as pd
from tradingview_screener import Query, Column

# Display markdown title
st.markdown("# Stock Screener")

# Get the number of rows and data from the Scanner
n_rows, data = (Query()
 .select('name', 'close', 'volume', 'pre-market_volume', 'relative_volume_10d_calc', 'average_volume')
 .where(
     Column('market_cap_basic').between(1_000_000, 50_000_000),
     Column('relative_volume_10d_calc') > 1.2,
     Column('MACD.macd') >= Column('MACD.signal')
 )
 .order_by('volume', ascending=False)
 .offset(5)
 .limit(25)
 .get_scanner_data())

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Ensure all columns have appropriate data types
# This step is crucial to avoid serialization issues
for column in df.columns:
    if df[column].dtype == 'object':
        df[column] = df[column].astype(str)

# Add a new column 'Issue' with the correct length
# Here we create a Series with the same length as the DataFrame
df["Issue"] = pd.Series([True, True, True, False] * (len(df) // 4) + [True] * (len(df) % 4))

# Display the DataFrame in Streamlit
st.write(df)




