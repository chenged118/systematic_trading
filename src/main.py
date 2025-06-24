# # src/main.py

# import yaml
# from src.utils.logger import setup_logger
# from src.strategies import get_strategy
# from src.core.engine import TradingEngine
# from src.executor.simulator import Simulator

# logger = setup_logger()

# def load_strategy_from_config(config: dict):
#     """
#     根據設定檔載入單一或多策略
#     """
#     strategy_cfg = config['strategies']
    
#     if isinstance(strategy_cfg, list):
#         # 多策略 → 使用 CompositeStrategy 包起來
#         from src.strategies.composite_strategy import CompositeStrategy

#         strategies = []
#         for strat in strategy_cfg:
#             strategy = get_strategy(
#                 name=strat['name'],
#                 **strat.get('params', {})
#             )
#             strategies.append(strategy)

#         return CompositeStrategy(strategies)
#     else:
#         # 單一策略
#         return get_strategy(
#             name=strategy_cfg['name'],
#             **strategy_cfg.get('params', {})
#         )

# def main():
#     logger.info("🚀 量化交易系統啟動")

#     # 載入設定
#     with open("config/settings.yaml", "r") as f:
#         config = yaml.safe_load(f)

#     # 載入策略（單一或多策略）
#     print("載入策略（單一或多策略）...")
#     strategy = load_strategy_from_config(config)

#     # 初始化執行器（模擬環境）
#     print("初始化執行器（模擬環境）...")
#     executor = Simulator()

#     # 建立交易引擎
#     print("建立交易引擎...")
#     engine = TradingEngine(strategy=strategy, executor=executor)

#     # 啟動主流程
#     print("啟動主流程...")
#     logger.info("交易引擎啟動中...")
#     engine.run()

# if __name__ == "__main__":
#     main()