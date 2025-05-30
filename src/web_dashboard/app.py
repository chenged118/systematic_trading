# src/web_dashboard/app.py

import sys
import os

# 將專案根目錄/src 加入 Python 模組搜尋路徑
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import yaml
import os
from glob import glob

from src.backtest.visualizer import plot_equity_curve
from src.core.engine import TradingEngine
from src.executor.simulator import Simulator
from src.strategies import get_strategies_from_config

st.set_page_config(page_title="量化策略 Dashboard", layout="wide")

st.title("📈 量化交易策略 Web Dashboard")

# 🔧 1. 選擇 Config 設定檔
st.sidebar.header("⚙️ 設定選擇")

config_files = glob("config/*.yaml")
selected_config = st.sidebar.selectbox("選擇策略設定檔", config_files)

if not selected_config:
    st.warning("請選擇一個設定檔")
    st.stop()

with open(selected_config, "r") as f:
    config = yaml.safe_load(f)

# 🔍 2. 載入策略與引擎
strategies_cfg = config.get("strategies", {})
strategy = get_strategies_from_config(strategies_cfg)
executor = Simulator()
engine = TradingEngine(strategy=strategy, executor=executor)

st.markdown(f"**目前策略：** `{strategy.name}`")

# 🚀 3. 執行回測按鈕
if st.button("🚀 執行回測"):
    with st.spinner("正在執行回測中..."):
        engine.run()

    st.success("✅ 回測完成")

    # 顯示報表與圖
    if os.path.exists("reports/backtest_summary.csv"):
        df = pd.read_csv("reports/backtest_summary.csv")
        plot_equity_curve(df)
        st.subheader("📊 回測績效摘要")
        st.dataframe(df)

        if "return" in df.columns and "win_rate" in df.columns:
            st.metric("總報酬率 (%)", f"{df['return'].values[0]:.2f}")
            st.metric("勝率 (%)", f"{df['win_rate'].values[0]:.2f}")

    if os.path.exists("reports/equity_curve.png"):
        st.subheader("💹 資金曲線")
        st.image("reports/equity_curve.png", use_column_width=True)
else:
    st.info("請按下上方按鈕開始回測")
    