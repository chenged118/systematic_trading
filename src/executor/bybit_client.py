import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

# 讀取 .env
load_dotenv()

# 判斷模式
mode = os.getenv("MODE")

if mode == "test":
    api_key = os.getenv("BYBIT_TEST_API_KEY")
    api_secret = os.getenv("BYBIT_TEST_API_SECRET")
    isTestnet = True
    # base_url = "https://api.bybit.com"  # ✅ 注意：這不是 testnet URL！
elif mode == "live":
    api_key = os.getenv("BYBIT_LIVE_API_KEY")
    api_secret = os.getenv("BYBIT_LIVE_API_SECRET")
    isTestnet = False
else:
    raise ValueError("Unknown MODE setting")

print("API Key: ", api_key)
print("API Secret: ", api_secret)
print("isTestnet: ", isTestnet)

session = HTTP(
    testnet=isTestnet,  # 使用 testnet
    api_key=api_key,
    api_secret=api_secret,
    # base_url=base_url  # 使用指定的 base_url
)


# 取得帳戶資訊
account_info = session.get_account_info()
print("account_info: ",  account_info)

wallet_balance = session.get_wallet_balance(accountType="UNIFIED")
print("wallet_balance: ",  wallet_balance)