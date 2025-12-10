import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import requests

# Compute SHA-256 checksum for a file
def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# Set up project directories

base_dir = Path(".").resolve()
data_dir = base_dir / "data"
raw_dir = data_dir / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)

checksums_dir = data_dir / "checksums.txt"

# Download Bitcoin price data from Yahoo Finance
yahoo_url = "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD"
params = {
    "interval": "1d",
    "range": "max"
}


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

r_price = requests.get(yahoo_url, params=params, headers=headers)
r_price.raise_for_status()
btc_price_data = r_price.json()

price_out_path = raw_dir / "btc_price_yahoo.json"
with price_out_path.open("w") as f:
    json.dump(btc_price_data, f)

price_checksum = sha256_of_file(price_out_path)
with checksums_dir.open("a") as f:
    f.write(f"{price_out_path.name}\t{price_checksum}\nYahooFinance\t{datetime.now(timezone.utc).isoformat()}\n")

# Download Bitcoin hashrate data from Blockchain.com
blockchain_url = "https://api.blockchain.info/charts/hash-rate"

params_hash = {
    "timespan": "all",   
    "format": "json",
}

r_hash = requests.get(blockchain_url, params=params_hash)
r_hash.raise_for_status()
btc_hashrate_data = r_hash.json()

hash_out_path = raw_dir / "btc_hashrate_blockchain.json"
with hash_out_path.open("w") as f:
    json.dump(btc_hashrate_data, f)

hash_checksum = sha256_of_file(hash_out_path)
with checksums_dir.open("a") as f:
    f.write(f"{hash_out_path.name}\t{hash_checksum}\nBlockchain.com\t{datetime.now(timezone.utc).isoformat()}\n")


print("Data Collection from API Succesfully Complete")
