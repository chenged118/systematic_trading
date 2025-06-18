# src/web_dashboard/Backtest.py

def run_backtest_dashboard():
    from glob import glob
    import sys
    import os

    # 將專案根目錄/src 加入 Python 模組搜尋路徑
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    import streamlit as st
    import pandas as pd
    import yaml
    import os
    from typing import List
    from data.loader import load_market_data
    from src.backtest.visualizer import plot_equity_curve
    from src.core.engine import TradingEngine
    from src.executor.simulator import Simulator
    from src.strategies import get_strategy  # 注意：這裡改為單一策略選擇

    # st.set_page_config(page_title="量化策略 Dashboard", layout="wide")

    st.title("📈 量化交易策略 Web Dashboard")

    # 🔧 1. 固定載入 config 設定檔
    CONFIG_PATH = "config/settings.yaml"

    if not os.path.exists(CONFIG_PATH):
        st.error(f"設定檔 {CONFIG_PATH} 不存在")
        st.stop()

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    # 🎛️ 顯示策略選單
    strategies_cfg: List[dict] = config.get("strategies", [])
    if not strategies_cfg:
        st.warning("設定檔中找不到任何策略")
        st.stop()

    strategy_names = [s["name"] for s in strategies_cfg]
    selected_name = st.sidebar.selectbox("選擇策略", strategy_names)

    # 根據選擇載入策略 config（params）
    selected_cfg = next((s for s in strategies_cfg if s["name"] == selected_name), None)
    if not selected_cfg:
        st.error(f"找不到策略設定：{selected_name}")
        st.stop()

    strategy = get_strategy(
        name=selected_cfg["name"],
        **selected_cfg.get("params", {})
    )

    # 🔧 2. 選擇資料檔案
    data_files = glob("data/raw/*.csv")
    selected_data_file = st.sidebar.selectbox("選擇市場資料 CSV 檔", data_files)

    if not selected_data_file:
        st.warning("請選擇一個市場資料檔案")
        st.stop()
        
    # ⚙️ 建立模擬執行器與交易引擎
    executor = Simulator()
    engine = TradingEngine(strategy=strategy, executor=executor)

    st.markdown(f"**目前策略：** `{strategy.name}`")

    # 🚀 3. 執行回測按鈕
    if st.button("🚀 執行回測"):
        with st.spinner("正在執行回測中..."):
            # 讀取市場資料
            data = load_market_data(selected_data_file)

            # 執行回測並傳入資料
            engine.run(data=data)

        st.success("✅ 回測完成")

        # 顯示報表與圖
        if os.path.exists("reports/trade_log.csv"):
            df = pd.read_csv("reports/trade_log.csv")
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
        