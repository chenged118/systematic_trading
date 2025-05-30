import pandas as pd

df = pd.read_csv("reports/backtest_summary.csv")
print("df.columns =", df.columns)
print(type(df))
print(df)
