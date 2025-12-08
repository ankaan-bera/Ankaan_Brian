from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm



base_dir = Path(".").resolve()
data_dir = base_dir / "data"
processed_dir = data_dir / "processed"
results_dir = base_dir / "results"
figures_dir = results_dir / "figures"
tables_dir = results_dir / "tables"

figures_dir.mkdir(parents=True, exist_ok=True)
tables_dir.mkdir(parents=True, exist_ok=True)


merged_data_path = processed_dir / "btc_merged.csv"
df = pd.read_csv(merged_data_path, parse_dates=["timestamp"])
df = df.set_index("timestamp").sort_index()


plt.figure()
plt.plot(df.index, df["price_btc"], label="BTC Price")
plt.title("Bitcoin Price Over Time")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plot_path = figures_dir / "btc_price.png"
plt.savefig(plot_path)
plt.close()

plt.figure()
plt.plot(df.index, df["hashrate_btc"], label="Hashrate Value")
plt.title("Bitcoin Hashrate Over Time")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plot_path = figures_dir / "btc_hashrate.png"
plt.savefig(plot_path)
plt.close()


df_norm = pd.DataFrame()
df_norm["price_norm"] = df["price_btc"] / df["price_btc"].iloc[0]
df_norm["hashrate_norm"] = df["hashrate_btc"] / df["hashrate_btc"].iloc[0]


plt.figure()
plt.plot(df_norm.index, df_norm["price_norm"], label="BTC Price (normalized)")
plt.plot(df_norm.index, df_norm["hashrate_norm"], label="BTC Hashrate (normalized)")
plt.title("Bitcoin Price and Hashrate (Normalized) Over Time")
plt.xlabel("Date")
plt.ylabel("Normalized Value")
plt.legend()
plt.tight_layout()
plot_path = figures_dir / "btc_price_hashrate_normalized.png"
plt.savefig(plot_path)
plt.close()


reg_df = df[["price_btc", "hashrate_btc"]].dropna()

x = sm.add_constant(reg_df["hashrate_btc"])
y = reg_df["price_btc"]

model = sm.OLS(y, x).fit()

summary_txt_path = tables_dir / "btc_regression_summary.txt"
with summary_txt_path.open("w") as f:
    f.write(model.summary().as_text())


params_df = model.params.to_frame(name="estimate")
params_df["std_err"]   = model.bse
params_df["t_value"]   = model.tvalues
params_df["p_value"]   = model.pvalues

params_csv_path = tables_dir / "btc_regression_results.csv"
params_df.to_csv(params_csv_path)


print("Plots and Linear Regression created succesfully")