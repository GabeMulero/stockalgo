import streamlit as st
import pandas as pd
from tradingview_screener import Scanner

# Display balloons animation
st.balloons()

# Display markdown title
st.markdown("# Stock Screener")

# Get the number of rows and data from the Scanner
n_rows, data = Scanner.premarket_gainers.get_scanner_data()

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

