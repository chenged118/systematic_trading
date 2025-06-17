# src/backtest/visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_equity_curve(df: pd.DataFrame, output_path="reports/equity_curve.png"):
    """
    根據績效 DataFrame 繪製資金曲線圖，並儲存成圖片檔
    """
    if "Cumulative PNL" not in df.columns:
        raise ValueError("資料中找不到 'Cumulative PNL' 欄位")

    # 繪圖
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["Cumulative PNL"], label="Cumulative PNL", color="blue", linewidth=2)
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Cumulative PNL")
    plt.grid(True)
    plt.legend()

    # 確保 reports 資料夾存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 儲存圖片
    plt.savefig(output_path)
    plt.close()