def run_autotrader():

    import streamlit as st
    import os
    import sys
    import pandas as pd
    from dotenv import load_dotenv

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

    # 3️⃣ 啟用／停用 自動交易
    st.subheader("⚙️ 自動交易狀態")

    if "auto_trade_enabled" not in st.session_state:
        st.session_state.auto_trade_enabled = False

    def toggle_autotrade():
        st.session_state.auto_trade_enabled = not st.session_state.auto_trade_enabled

    btn_label = "✅ 停止自動交易" if st.session_state.auto_trade_enabled else "🚀 啟動自動交易"
    if st.button(btn_label):
        toggle_autotrade()

    status = "🟢 已啟動" if st.session_state.auto_trade_enabled else "🔴 未啟動"
    st.write(f"目前狀態：{status}")

    # 4️⃣ 顯示當前訂單狀態
    st.subheader("📦 當前訂單狀態")
    try:
        orders = executor.get_open_orders()
        if orders:
            order_df = pd.DataFrame(orders)
            st.dataframe(order_df[["orderId", "symbol", "side", "orderType", "qty", "price", "orderStatus"]])
        else:
            st.info("目前沒有任何開倉中的訂單。")
    except Exception as e:
        st.error(f"❌ 無法取得訂單資訊：{e}")