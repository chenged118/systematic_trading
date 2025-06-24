# src/strategies/__init__.py

from .base import BaseStrategy
from .test_strategy import TestStrategy
from .my_strategy import MyStrategy
from .mean_reversion import MeanReversionStrategy
from .composite_strategy import CompositeStrategy
from .macd_strategy import MACDStrategy
from .breakout import BreakoutStrategy

STRATEGY_REGISTRY = {
    "test": TestStrategy,  # 測試用策略
    "my": MyStrategy,
    "mean_reversion": MeanReversionStrategy,
    "macd": MACDStrategy,
    "composite": CompositeStrategy,
    "breakout": BreakoutStrategy,
    # 可擴充：另一個策略
    # "another_strategy": AnotherStrategy,
}

def get_strategy(name: str, **kwargs) -> BaseStrategy:
    if name not in STRATEGY_REGISTRY:
        raise ValueError(f"❌ 未註冊策略：{name}")
    return STRATEGY_REGISTRY[name](**kwargs)

def get_strategy_names():
    return list(STRATEGY_REGISTRY.keys())

def get_strategies_from_config(strategy_cfg: dict) -> BaseStrategy:
    if isinstance(strategy_cfg, list):
        # 多策略 → 使用 CompositeStrategy 包起來
        strategies = []
        for strat in strategy_cfg:
            strategy = get_strategy(
                name=strat["name"],
                **strat.get("params", {})
            )
            strategies.append(strategy)
        return CompositeStrategy(strategies)
    else:
        # 單一策略
        return get_strategy(
            name=strategy_cfg["name"],
            **strategy_cfg.get("params", {})
        )
    
__all__ = ["get_strategy", "get_strategy_from_config"]