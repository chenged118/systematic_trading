# src/web_dashboard/Home.py
import streamlit as st
import yaml
import pandas as pd
from src.executor.bybit_executor import BybitExecutor  # 你需自行實作
from src.core.engine import TradingEngine
from src.strategies import get_strategies_from_config

st.title("📡 自動交易頁面")

# 選擇設定檔
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

strategies_cfg = config.get("strategies", {})
strategy = get_strategies_from_config(strategies_cfg)

# 建立 bybit 交易執行器
executor = BybitExecutor(api_key=..., api_secret=..., endpoint=...)

# 建立引擎
engine = TradingEngine(strategy=strategy, executor=executor)

if st.button("🚀 啟動自動交易"):
    engine.run()
    st.success("✅ 自動交易已啟動")