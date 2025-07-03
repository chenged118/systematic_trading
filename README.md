# 📈 系統化量化交易系統

這是一個基於 Python、Bybit API 與 Streamlit 打造的量化交易系統，包含：

✅ 策略模組化  
✅ 回測引擎  
✅ Bybit 模擬/實盤自動交易  
✅ 訂單即時監控 (WebSocket)  
✅ 完整 Web Dashboard 操作介面

---

## ⚙️ 安裝

1️⃣ 安裝 Python 3.9+  
2️⃣ 安裝相依套件：

```bash
pip install -r requirements.txt

```

3️⃣ 設定 Bybit API 金鑰，建立 .env 檔：

```.env
MODE=test
BYBIT_TEST_API_KEY=你的Testnet API Key
BYBIT_TEST_API_SECRET=你的Testnet API Secret

# 若要使用實盤
# MODE=live
# BYBIT_LIVE_API_KEY=你的Live API Key
# BYBIT_LIVE_API_SECRET=你的Live API Secret
```

## 🔧 設定策略

透過 config/settings.yaml 設定可用策略與參數，例如：

```
strategies:
  - name: macd_strategy
    params:
      fast_period: 12
      slow_period: 26
      signal_period: 9
  - name: breakout
    params:
      threshold: 0.02
```

## 🚀 啟動 Dashboard

執行：

```bash
streamlit run streamlit_app.py
```

打開瀏覽器 http://localhost:8501，即可進入多頁面 Dashboard：

✅ 首頁：導引與系統狀態
✅ 回測頁：選擇策略、載入資料並執行回測
✅ 自動交易頁：選擇策略後啟動自動交易服務，顯示帳戶餘額、歷史交易紀錄、即時訂單狀態

## 🛠 功能說明

✅ 自動交易服務
• 在自動交易頁面選擇策略與停損參數後，點擊「啟動自動交易」即可開始。
• 背景執行 AutoTraderService，持續獲取行情、產生交易信號並下單。
• 訂單結果即時回饋到頁面。

✅ 訂單即時監控
• 透過 WebSocket 連接 Bybit Private Stream，顯示 order、execution 訂單狀態更新。

✅ 回測引擎
• 使用 TradingEngine 模組化接入策略與模擬執行器，執行歷史資料回測並產生報告、資金曲線。

## 💡 常見問題

✅ Market Order 無法下單？
Bybit Testnet 市價單有最小金額限制，通常需超過 10 USDT，否則會回傳 Order value exceeded lower limit。

✅ 無法取得帳戶餘額？
請確認 Bybit Testnet API Key 權限設定為「讀取」與「交易」。

✅ WebSocket 沒有回應訂單更新？
請確認你的 API Key 為同一帳號，且成功認證後已訂閱 order / execution topic。

## 📜 參考資源

[Bybit API 官方文件](https://bybit-exchange.github.io/docs/)

[Bybit Testnet 平台](https://testnet.bybit.com/en/)
