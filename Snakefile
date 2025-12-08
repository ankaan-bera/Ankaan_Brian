# Snakefile

# Final targets we want:
rule all:
    input:
        "data/processed/btc_merged.csv",
        "results/tables/btc_data_quality_summary.csv",
        "results/figures/btc_price_hashrate_normalized.png",
        "results/figures/btc_price.png",
        "results/figures/btc_hashrate.png",
        "results/tables/btc_regression_results.csv",
        "results/tables/btc_regression_summary.txt"


rule data:
    output:
        "data/raw/btc_price_yahoo.json",
        "data/raw/btc_hashrate_blockchain.json",
        "data/checksums.txt"
    shell:
        "python scripts/data_01.py"


rule integrate_clean:
    input:
        "data/raw/btc_price_yahoo.json",
        "data/raw/btc_hashrate_blockchain.json"
    output:
        "data/processed/btc_merged.csv",
        "results/tables/btc_data_quality_summary.csv"
    shell:
        "python scripts/clean_integrate_02.py"


rule analyze:
    input:
        "data/processed/btc_merged.csv"
    output:
        "results/figures/btc_price_hashrate_normalized.png",
        "results/figures/btc_price.png",
        "results/figures/btc_hashrate.png",
        "results/tables/btc_regression_results.csv",
        "results/tables/btc_regression_summary.txt"
    shell:
        "python scripts/analyze_03.py"
