def run_autotrader():

    import streamlit as st
    import os
    import sys
    import pandas as pd
    from dotenv import load_dotenv

    from src.auto_trader.order_ws import start_ws
    from src.auto_trader.state import state
    from src.auto_trader.auto_trader_service import AutoTraderService
    from src.strategies import get_strategy_names
    from streamlit_autorefresh import st_autorefresh

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from src.executor.bybit_executor import BybitExecutor


    executor = BybitExecutor()  # 或傳入 API key/secret

    # 讀取環境變數
    load_dotenv()

    # 設定 Streamlit 頁面
    # st.set_page_config(page_title="自動交易系統", layout="wide")

    from pybit.unified_trading import HTTP

    # 初始化 API session
    mode = os.getenv("MODE")
    if mode == "test":
        api_key = os.getenv("BYBIT_TEST_API_KEY")
        api_secret = os.getenv("BYBIT_TEST_API_SECRET")
        isTestnet = True
    elif mode == "live":
        api_key = os.getenv("BYBIT_LIVE_API_KEY")
        api_secret = os.getenv("BYBIT_LIVE_API_SECRET")
        isTestnet = False
    else:
        st.error("未正確設定 .env 中的 MODE。請設為 test 或 live。")
        st.stop()

    session = HTTP(
        testnet=isTestnet,
        api_key=api_key,
        api_secret=api_secret
    )

    st.title("🤖 自動交易 Dashboard")

    # 1️⃣ 顯示帳戶餘額
    st.subheader("💰 帳戶餘額")
    try:
        wallet_balance_infos = session.get_wallet_balance(accountType="UNIFIED")
        balance = float(wallet_balance_infos["result"]["list"][0]["totalWalletBalance"])
        st.metric(label="總餘額", value=f"{balance:.2f}")
        # usdt_balance = float(balances["result"]["list"][0]["coin"][0])
        # st.metric(label="USDT 餘額", value=f"{usdt_balance:.2f}")
    except Exception as e:
        st.error(f"無法取得餘額：{e}")

    # 2️⃣ 顯示歷史交易紀錄
    st.subheader("📜 歷史交易紀錄")
    try:
        trade_df = executor.get_trade_history(symbol="BTCUSDT", limit=50)

        if trade_df.empty:
            st.info("目前尚無交易紀錄。")
        else:
            st.dataframe(trade_df)
    except Exception as e:
        st.error(f"❌ 無法取得歷史交易紀錄：{e}")

    # # 3️⃣ 啟用／停用 自動交易
    # st.subheader("⚙️ 自動交易狀態")

    # if "auto_trade_enabled" not in st.session_state:
    #     st.session_state.auto_trade_enabled = False

    # def toggle_autotrade():
    #     st.session_state.auto_trade_enabled = not st.session_state.auto_trade_enabled

    # btn_label = "✅ 停止自動交易" if st.session_state.auto_trade_enabled else "🚀 啟動自動交易"
    # if st.button(btn_label):
    #     toggle_autotrade()

    # status = "🟢 已啟動" if st.session_state.auto_trade_enabled else "🔴 未啟動"
    # st.write(f"目前狀態：{status}")

    # 3️⃣ 啟用／停用 自動交易
    st.subheader("⚙️ 自動交易狀態")

    # 🎯 策略選擇
    all_strategies = get_strategy_names()  # 回傳像 ["SmaCross", "RsiStrategy"]
    selected_strategy = st.selectbox("選擇策略", all_strategies)

    # 🎯 停損參數設定
    stop_loss_pct = st.slider("停損百分比 (%)", min_value=0.0, max_value=0.2, value=0.05, step=0.01)

    # 🟢 啟動／關閉自動交易
    if not state.is_running:
        if st.button("🚀 啟動自動交易"):
            state.service = AutoTraderService(
                strategy_name=selected_strategy,
                stop_loss_pct=stop_loss_pct,
                interval_sec=10
            )
            state.service.start()
            state.is_running = True
            st.success(f"✅ 自動交易已啟動（策略：{selected_strategy}）")
    else:
        if st.button("🛑 停止自動交易"):
            if state.service:
                state.service.stop()
            state.is_running = False
            state.service = None
            st.warning("🛑 自動交易已停止")

    # 📊 狀態顯示
    st.write(f"目前狀態：{'🟢 已啟動' if state.is_running else '🔴 未啟動'}")

    # 4️⃣ 顯示當前掛單狀態
    st.subheader("📡 當前掛單狀態")
    try:
        open_orders_df = executor.get_open_orders(symbol="BTCUSDT", category="linear")
        if not open_orders_df.empty:
            st.dataframe(open_orders_df)
        else:
            st.info("目前沒有掛單。")
    except Exception as e:
        st.error(f"無法取得掛單資訊：{e}")

    # ✅ 啟動 WebSocket
    start_ws()

    # ✅ 自動刷新畫面
    st_autorefresh(interval=5000, key="autorefresh")

    # 4️⃣ 顯示當前訂單狀態
    # st.subheader("📦 當前訂單狀態")
    # try:
    #     orders = executor.get_open_orders()
    #     if orders:
    #         order_df = pd.DataFrame(orders)
    #         st.dataframe(order_df[["orderId", "symbol", "side", "orderType", "qty", "price", "orderStatus"]])
    #     else:
    #         st.info("目前沒有任何開倉中的訂單。")
    # except Exception as e:
    #     st.error(f"❌ 無法取得訂單資訊：{e}")

    st.subheader("📡 最新訂單狀態")
    
    if state.order_logs:
        df = pd.DataFrame(state.order_logs)
        
        # 顯示選擇欄位與排序
        cols = ["topic", "symbol", "side", "orderType", "price", "qty", "orderStatus", "timestamp"]
        display_df = df[[col for col in cols if col in df.columns]].copy()

        # 時間格式
        display_df["timestamp"] = pd.to_datetime(display_df["timestamp"], unit="s")
        display_df = display_df.sort_values("timestamp", ascending=False).head(10)

        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("尚無訂單狀態更新")