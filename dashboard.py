import json
import streamlit as st
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
from WallStreet.app import db
from WallStreet.models import Watchlist
import yfinance as yf
import plotly.express as px
from flask_login import current_user
import requests

st.title("Stocks Dashboard")

api_key = 'PX1DL0VXFFYGTEMH'
api_url = 'http://127.0.0.1:5000/api/get_user_info'


def authenticate_user():
    response = requests.get(api_url)
    
    if not response.content:
        return False

    try:
        data = response.json()
    except json.JSONDecodeError:
        data = {'error': 'Invalid JSON'}

    print(f'Response content: {response.content}')

    if 'text/html' in response.headers.get('content-type', ''):
        return False

    return data.get('authenticated', False)


def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def get_intraday_data(symbol, interval, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval)
    return data

def fetch_time_series(symbol, interval='5min'):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval)
    return data['4. close']

def main():
    if authenticate_user() is True:
        st.sidebar.header("Watchlist Management")
        watchlist_symbols = st.sidebar.text_input("Watchlist Symbols (comma-separated):")
        watchlist_symbols = [symbol.strip().upper() for symbol in watchlist_symbols.split(',')]

        st.sidebar.header("Filter Criteria")
        start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
        end_date = st.sidebar.date_input("End Date", datetime.now())
        selected_interval = st.sidebar.selectbox("Select Time Interval:", ['5min'], index=0)

        st.header("Historical Stock Data")

        for symbol in watchlist_symbols:
            stock_data = get_stock_data(symbol, start_date, end_date)
            st.subheader(f"{symbol} Historical Stock Data")
            st.write(stock_data)

            fig = px.candlestick(stock_data, x=stock_data.index, open='Open', high='High', low='Low', close='Close', title=f'{symbol} Stock Price (Historical)')
            st.plotly_chart(fig)

        st.header("Intraday Stock Data")

        for symbol in watchlist_symbols:
            intraday_data = get_intraday_data(symbol, selected_interval, api_key)
            st.subheader(f"{symbol} Intraday Stock Data")
            st.write(intraday_data)

            intraday_fig = px.line(intraday_data, x=intraday_data.index, y='4. close', title=f'{symbol} Intraday Stock Price')
            st.plotly_chart(intraday_fig)
    else:
        st.warning("Please log in to access the dashboard.")
        
        
print(authenticate_user())

if __name__ == "__main__":
    main()
