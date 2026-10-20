"""Historical closing-price comparison of five technology companies (2013–2018)."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
SYMBOLS = ["GOOGL", "FB", "AAPL", "AMZN", "MSFT"]
prices = {}
for symbol in SYMBOLS:
    df = pd.read_csv(BASE / "data" / f"{symbol}_data.csv", parse_dates=["date"])
    df = df.sort_values("date").drop_duplicates("date").set_index("date")
    prices[symbol] = df["close"]
closing = pd.DataFrame(prices).dropna()
returns = closing.pct_change().dropna()
normalized = closing.div(closing.iloc[0]).mul(100)
summary = pd.DataFrame({
    "start_close": closing.iloc[0], "end_close": closing.iloc[-1],
    "price_change_pct": (closing.iloc[-1] / closing.iloc[0] - 1) * 100,
    "daily_volatility_pct": returns.std() * 100
}).sort_values("price_change_pct", ascending=False)
summary.round(3).to_csv(BASE / "summary.csv", index_label="ticker")
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10,5.5))
for symbol in SYMBOLS:
    ax.plot(normalized.index, normalized[symbol], label=symbol, linewidth=1.8)
ax.set(title="Indexed closing prices (Feb 2013–Feb 2018)",ylabel="Price index (first day = 100)",xlabel="Date")
ax.legend(ncol=5, loc="upper left"); fig.autofmt_xdate(); fig.tight_layout()
fig.savefig(BASE / "figures" / "normalized_price_trends.png",dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(9,5))
vol=summary["daily_volatility_pct"].sort_values()
bars=ax.barh(vol.index,vol.values,color="#3a719c")
for bar,v in zip(bars,vol.values): ax.text(v+.025,bar.get_y()+bar.get_height()/2,f"{v:.2f}%",va="center")
ax.set(xlim=(0,max(vol)*1.2), xlabel="Standard deviation of daily close-to-close returns (%)",title="Daily return volatility (Feb 2013–Feb 2018)")
fig.tight_layout(); fig.savefig(BASE / "figures" / "daily_volatility.png",dpi=160); plt.close(fig)
print(summary.round(2).to_string())
print("Created summary.csv and two figures in figures/.")
