from pathlib import Path
import json
from datetime import datetime, timezone
import pandas as pd


base_dir = Path(".").resolve()
data_dir = base_dir / "data"
raw_dir = data_dir / "raw"
processed_dir = data_dir / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

results_dir = base_dir / "results"
tables_dir = results_dir / "tables"
tables_dir.mkdir(parents=True, exist_ok=True)

start_dt = datetime(2018, 1, 1, tzinfo=timezone.utc)
end_dt   = datetime(2023, 1, 1, tzinfo=timezone.utc)   


price_path = raw_dir / "btc_price_yahoo.json"
with price_path.open() as f:
    price_raw = json.load(f)


result = price_raw["chart"]["result"][0]
timestamps = result["timestamp"]
quotes = result["indicators"]["quote"][0]
closes = quotes["close"]

price_df = pd.DataFrame({
    "timestamp": pd.to_datetime(timestamps, unit="s", utc=True),
    "price_btc": closes,
})


price_df = price_df.dropna(subset=["price_btc"])
price_df = price_df.set_index("timestamp")
price_df = price_df.sort_index()

price_df = price_df.resample("1D").ffill()


hash_path = raw_dir / "btc_hashrate_blockchain.json"
with hash_path.open() as f:
    hash_raw = json.load(f)

hash_df = pd.DataFrame(hash_raw["values"])
hash_df["timestamp"] = pd.to_datetime(hash_df["x"], unit="s", utc=True)
hash_df = hash_df.set_index("timestamp")
hash_df = hash_df.drop(columns=["x"])
hash_df = hash_df.rename(columns={"y": "hashrate_btc"})

hash_df = hash_df.resample("1D").ffill()

merged = price_df.join(hash_df, how="inner")
merged = merged.sort_index()


interval = (merged.index >= start_dt) & (merged.index < end_dt)
merged = merged.loc[interval]

merged["date"] = merged.index.date

out_path = processed_dir / "btc_merged.csv"
merged.to_csv(out_path, index_label="timestamp")


rows = []
for col in merged.columns:
    s = merged[col]
    rows.append({
        "column": col,
        "dtype": str(s.dtype),
        "num_non_null": int(s.notna().sum()),
        "num_null": int(s.isna().sum()),
        "min": s.min() if s.notna().any() else None,
        "max": s.max() if s.notna().any() else None,
    })

quality_df = pd.DataFrame(rows)
quality_out = tables_dir / "btc_data_quality_summary.csv"
quality_df.to_csv(quality_out, index=False)


print("Data Cleaned and Integrated Succesfully")