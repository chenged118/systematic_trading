import websocket
import threading
import json
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv

from src.auto_trader.state import state

load_dotenv()

def get_auth_headers():
    api_key = os.getenv("BYBIT_TEST_API_KEY")
    api_secret = os.getenv("BYBIT_TEST_API_SECRET")
    expires = int(time.time() * 1000) + 10000
    signature_payload = f"GET/realtime{expires}"
    signature = hmac.new(
        api_secret.encode(),
        signature_payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return {
        "api_key": api_key,
        "expires": expires,
        "signature": signature
    }

def on_message(ws, message):
    data = json.loads(message)

    # 保留訂單 / 成交記錄
    topic = data.get("topic")
    if topic and topic.startswith(("order.", "execution.")):
        rows = data.get("data", [])
        if isinstance(rows, dict):
            rows = [rows]  # 包成 list
        for row in rows:
            row["topic"] = topic
            row["timestamp"] = int(time.time())
            state.order_logs.append(row)

        # 只保留最近 50 筆
        if len(state.order_logs) > 50:
            state.order_logs = state.order_logs[-50:]

def on_open(ws):
    print("✅ WebSocket 已連線")

    # 認證
    auth = get_auth_headers()
    ws.send(json.dumps({
        "op": "auth",
        "args": [auth["api_key"], auth["expires"], auth["signature"]]
    }))

    # 訂閱所有類別（合約 + 現貨）
    ws.send(json.dumps({
        "op": "subscribe",
        "args": [
            "order.spot", "execution.spot",
            # "order.linear", "execution.linear",
            # "order.inverse", "execution.inverse"
        ]
    }))

def start_ws():
    mode = os.getenv("MODE")
    if mode == "test":
        ws_url = "wss://stream-testnet.bybit.com/v5/private"  # Unified Account private stream
    elif mode == "live":
        ws_url = "wss://stream.bybit.com/v5/private"  # Unified Account private stream
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()