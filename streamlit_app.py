import streamlit as st
import pandas as pd
from tradingview_screener import Query, Column
import requests

# Display markdown title
st.markdown("# Stock Screener")

try:
    # Get the number of rows and data from the Scanner
    n_rows, data = (Query()
        .select('exchange','name', 'close', 'volume', 'average_volume','relative_volume_10d_calc', 'Volatility.D', 'change')
        .where(
            Column('market_cap_basic').between(200_000_000, 10_000_000_000),
            Column('relative_volume_10d_calc') > 1.2,
            Column('change') >= 10
        
        )
        .order_by('volume', ascending=False)
        .offset(5)
        .limit(25)
        .get_scanner_data())

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Ensure all columns have appropriate data types
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].astype(str)


    df = df[df['exchange'] != 'OTC']        

    # Add a new column 'Issue' with the correct length
    df["Issue"] = pd.Series([True, True, True, False] * (len(df) // 4) + [True] * (len(df) % 4))

    # Display the DataFrame in Streamlit
    st.write(df)

except requests.exceptions.HTTPError as e:
    st.error(f"HTTP Error: {e}")
    st.error(f"Status code: {e.response.status_code}")
    st.error(f"Reason: {e.response.reason}")
except requests.exceptions.RequestException as e:
    st.error(f"Request Error: {e}")