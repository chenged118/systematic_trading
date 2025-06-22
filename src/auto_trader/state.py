# src/auto_trader/state.py

from types import SimpleNamespace

state = SimpleNamespace(
    is_running=False,
    service=None,
    order_logs=[]  # 加入 WebSocket 訂單狀態用
)