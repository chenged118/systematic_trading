# streamlit_app.py

import streamlit as st
import os
import sys

# 把 src 加入 path，讓 Python 能夠 import src.*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# 頁面設定
st.set_page_config(page_title="量化交易系統", layout="wide")

# 側邊欄選單
st.sidebar.title("📊 功能選單")
page = st.sidebar.radio("請選擇功能頁面", ["首頁", "自動交易", "歷史回測"])

# 頁面內容
if page == "首頁":
    st.title("🎛 歡迎使用量化交易系統 Dashboard")
    st.markdown("請從左側選單選擇功能：")

elif page == "自動交易":
    st.title("🤖 自動交易")
    st.info("此頁面將串接 Bybit 並進行下單。")
    from src.auto_trader.auto_trader import run_autotrader
    run_autotrader()

elif page == "歷史回測":
    st.title("📈 歷史資料回測")
    st.info("此頁面將讀取歷史資料並進行策略回測。")
    from src.web_dashboard.Backtest import run_backtest_dashboard
    run_backtest_dashboard()
    