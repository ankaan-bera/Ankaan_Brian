# Bitcoin Price and Network Hashrate: An Empirical Relationship (2018–2023)

---

## Contributors
- Brian Jett  
- Ankaan Bera

---

## Summary

Bitcoin sits in an odd place: it is both a speculative financial asset and a physically secured computational network. Those two sides of the system are usually talked about separately. Traders focus on the price chart, miners think about hash power and electricity costs, and most people pick one lens or the other. In reality, price and hashrate are linked by a pretty direct incentive loop. When the price runs up, mining revenue rises, new hardware comes online, and the network becomes more secure. When the price collapses, some miners capitulate, but a surprising amount of hash power tends to stick around. This project is about quantifying that relationship over a recent five-year window.

The central question we try to answer is simple but meaningful: **to what extent does Bitcoin’s network security, measured by hashrate, explain its market price between 2018 and 2023?** We are not trying to build a trading model or pretend that hashrate is the only thing that matters. Instead, we want to see how far we can get with a disciplined dataset, basic regression, and a fully reproducible pipeline.

We start by collecting two datasets programmatically. Daily BTC-USD price data comes from the Yahoo Finance chart API. Daily Bitcoin hashrate data comes from the Blockchain.com charts API. Both are downloaded as JSON and written into a `data/raw` folder by a script that also computes a SHA-256 checksum for each file and logs the hash, the source, and the UTC timestamp in `data/checksums.txt`. That checksum log means anyone re-running our workflow can confirm they are using the exact same raw inputs we did, down to the byte.

The second step is cleaning and integration. A separate script reads the two raw JSON files, converts Unix timestamps to UTC datetimes, and extracts the daily closing price (`price_btc`) and estimated network hashrate (`hashrate_btc`). We drop obvious nulls, convert both series to a daily time index, and forward-fill to avoid gaps. Then we restrict the data to a shared window between January 1, 2018 and January 1, 2023. This gives us 1,826 joint daily observations that cover the 2018 bear market, the slow 2019 recovery, the COVID liquidity run-up, the 2021 peak, and the 2022 drawdown. The merged dataset is written to `data/processed/btc_merged.csv`.

With the data in one place, we move to analysis. We generate three plots: Bitcoin price over time, Bitcoin hashrate over time, and a normalized comparison where both series are scaled to 1 at the start of 2018. The figures make the basic story visually obvious. Price behaves like a classic speculative asset: long periods of grinding followed by violent vertical moves and equally sharp crashes. Hashrate, by contrast, behaves like capital stock. It grows steadily, takes a hit in mid-2021 when China shuts down mining, then recovers and keeps climbing.

To put a number on the relationship, we fit an ordinary least squares regression of daily price on daily hashrate. The model is intentionally simple: price is the dependent variable, hashrate is the lone regressor, and we include a constant. We are not correcting for autocorrelation or building a full time-series model here; the point is to see how much variation in price is lined up with variation in hashrate at a basic level.

The result is a positive and highly statistically significant association. The estimated slope on hashrate is positive, the t-statistic is large, and the p-value is effectively zero. Roughly 30% of the cross-sample variation in daily price is associated with changes in daily hashrate. That is a lot, considering the model ignores everything else going on in crypto markets, global macro, and regulation. At the same time, 70% of the variation is still left on the table, which is exactly what you would expect for an asset that lives and dies by sentiment and liquidity as much as fundamentals.

The broader takeaway is not that “hashrate predicts price” in some mechanical way. Instead, the evidence points to a long-run coupling between the financial side of Bitcoin and the physical side. Over multi-year horizons, when the network is accumulating more hash power, price tends to live in a higher regime. Short-run swings, bubbles, and crashes ride on top of that relationship and are driven by many other forces we do not model here.

Just as important as the regression itself is how we get to it. The project is implemented as a small, end-to-end data pipeline: programmatic acquisition, cryptographic integrity checks, deterministic cleaning, integration, visualization, and modeling. Anyone with Python and the listed dependencies can clone the repository, re-run the three scripts, and regenerate the exact same figures and regression outputs. So the project is both a case study of Bitcoin’s incentive structure and a concrete example of reproducible computational work.

## Data Profile

The project is built on two main datasets, both of which are publicly available and describe different layers of the same system. One lives in markets (price), the other in infrastructure (hashrate). The whole analysis is about stitching those two together in a way that is clean and defensible.

**Bitcoin price (Yahoo Finance)**  
The first dataset is daily BTC-USD price data pulled from the Yahoo Finance chart API. We call the endpoint for the `BTC-USD` symbol and request the full available range at a one-day interval. The API returns a JSON object with a list of Unix timestamps and several arrays of OHLC values. From that, we extract the closing price and convert the timestamps to timezone-aware UTC datetimes. This gives us a time series of daily closing prices, which we store as `price_btc`. The raw JSON response is written to `data/raw/btc_price_yahoo.json` and never edited manually.

After loading, we do a small amount of cleaning. Any rows where the close price is missing are dropped, since a missing close has no obvious interpretation. We then set the timestamp as the index, sort by time, and resample to exactly daily frequency using forward fill. Forward filling is a conscious choice: Bitcoin trades essentially nonstop, and the few gaps that appear at daily resolution are usually reporting artifacts rather than genuine “no trading” days. The resampled series is therefore a smooth daily trace of market prices.

**Bitcoin hashrate (Blockchain.com)**  
The second dataset is daily estimated Bitcoin hashrate from Blockchain.com’s charts API. This endpoint returns a JSON object with a list of `(x, y)` points, where `x` is a Unix timestamp and `y` is the estimated network hash power at that time. We convert the timestamps to UTC datetimes, drop the raw `x` column, and rename `y` to `hashrate_btc`. As with price, the raw JSON file (`data/raw/btc_hashrate_blockchain.json`) is kept intact.

We resample the hashrate series to a daily frequency and forward-fill here as well. The reasoning is similar but even stronger: hashrate changes as miners plug in or unplug ASICs, but at the granularity of days the network evolves relatively smoothly. The resampled series captures that slow evolution while smoothing out reporting noise.

**Integration window and merged dataset**  
Both datasets are then restricted to a shared window that runs from January 1, 2018 through January 1, 2023. That choice is intentional. The period includes multiple full price cycles, a major exogenous policy shock (the 2021 Chinese mining crackdown), and enough time for mining infrastructure to grow by an order of magnitude. We keep only dates that appear in both time series using an inner join on the timestamp index. The result is a merged table with 1,826 rows and three columns: `price_btc`, `hashrate_btc`, and a calendar `date` derived from the timestamp.

The merged dataset is written to `data/processed/btc_merged.csv` and is the single source of truth for downstream analysis. Scripts that generate plots or run regression never reach back into the raw JSON files. That separation makes it very clear where cleaning ends and analysis begins.

**Ethics, legality, and access**  
Both data sources are public and aggregate. There is no personal or sensitive information anywhere in the pipeline. Yahoo Finance and Blockchain.com expose this data specifically for analysis and visualization, and the project uses the data in that spirit: educational, non-commercial, and reproducible. Because we pull the data programmatically, anyone re-running the scripts can obtain the same inputs (subject to the providers keeping their endpoints stable).

**Provenance and integrity**  
As a final layer, every raw file we download is hashed using SHA-256. We record the filename, the hash, the upstream source, and the UTC retrieval time in `data/checksums.txt`. That log is effectively a minimal provenance record for the project. If the APIs change or the files get corrupted, the hashes will no longer match, and we will know something is off. It also gives the TAs a straightforward way to verify they are grading against the same inputs we used when we wrote the report.

## Data Quality

Once the price and hashrate data are merged, we take a step back and ask a basic question: is this dataset stable and well-behaved enough that we can trust any patterns we see? To answer that, the cleaning script builds a simple column-level profile and writes it to `results/tables/btc_data_quality_summary.csv`. The profile records each column’s data type, the number of non-null and null entries, and the minimum and maximum observed values.

The first thing to notice is that both `price_btc` and `hashrate_btc` are complete after preprocessing. For the 1,826 dates in our integration window, neither column has missing values. That is not something we get for free from the APIs; it is the result of explicitly dropping obviously broken observations and then resampling with forward fill so that every day in the window has a defined price and hashrate. We also carry a `date` column derived from the timestamp purely for readability; that column is complete as well.

The ranges of the two numeric variables line up with what you would expect from real Bitcoin history. The minimum daily closing price in the window is a bit above $3,450 and the maximum daily close is a little over $61,000. Those values correspond to the late-2018 bear market lows and the late-2021 highs. There are no bizarre outliers where the price is, say, a fraction of a cent or several hundred thousand dollars. That is a quick sanity check that we have not mis-parsed the JSON or mistaken some other field for the close.

The hashrate series tells a similar story. The minimum observed value is on the order of fifteen million (in the same units as the API reports) and the maximum is just over three hundred million. The trajectory between those endpoints is not linear, but it is monotonic enough that you can see a clear long-run upward drift in the time-series plot. That matches the basic narrative that mining capacity has expanded massively as industrial players have entered the space. One striking feature is the visible drop in mid-2021, which lines up with the Chinese mining crackdown. The fact that this event shows up exactly where it should, and with a plausible magnitude, is a strong external validity check on the data.

None of this means the dataset is “perfect.” There are built-in limitations we cannot eliminate with cleaning. Hashtate is an estimate inferred from block production, not a direct meter reading of every ASIC on earth. Price is a single synthetic series that stands in for a fragmented global market where liquidity and microstructure change over time. Both series are highly persistent, which shows up clearly in the regression diagnostics: the Durbin–Watson statistic for our OLS fit is roughly 0.012, signaling strong positive autocorrelation in the residuals. That is to be expected with daily financial data, but it also tells us that we should be careful about treating the regression as a full structural model.

So the right way to summarize data quality here is: **mechanically clean, structurally reasonable, but economically complex**. Mechanically, we have no missing values in the final dataset, well-typed columns, and plausible value ranges that line up with known historical events. Structurally, the patterns we see in the plots—gradual hashrate growth with a dip in 2021, price booms and busts around 2020–2021—are exactly what you would expect from anyone who has watched Bitcoin for the last few years. Economically, the data are noisy because the underlying system is noisy. There is no cleaning step that can make Bitcoin less volatile or mining less path-dependent.

For the purposes of this project, this level of quality is enough. The data are coherent, reproducible, and anchored to real events. Any caveats we need to carry come from the nature of the asset, not from bugs in our pipeline.

## Findings

The easiest way to understand the results is to start with the plots and then move to the regression. The raw price chart looks like what you would expect from a highly speculative asset. Starting in early 2018, the price grinds downward out of the 2017 bubble, bottoms out in the $3–4k range, and then slowly rebuilds a base. The 2020–2021 stretch is almost vertical, with a sequence of sharp rallies and pullbacks, followed by a long, painful slide through 2022. It is a visual reminder that daily Bitcoin returns are not gentle.

The hashrate plot tells a different story. Instead of jagged price action, you see a long-run upward ramp in network hash power. There are fluctuations, but the main pattern is growth. The single obvious exception is the sharp drop in mid-2021 when China forced a large number of miners offline. Even there, the cut is temporary: hashrate recovers and eventually exceeds the pre-ban level as mining capacity relocates geographically. From a systems point of view, it looks a lot more like capital stock accumulation than like a tradeable asset.

The normalized comparison plot is where the two stories collide. When we scale both series to 1 at the start of 2018, price and hashrate move together for a while, but price repeatedly overshoots, collapses, and overshoots again. Hashrate, on the other hand, mostly keeps grinding higher. That picture is the whole argument of the project in one panel: the financial side of Bitcoin is chaotic; the physical side is slow, sticky, and surprisingly resilient.

The regression puts a number on the relationship. We fit an OLS model where daily `price_btc` is regressed on `hashrate_btc` with a constant. The estimated intercept is about 4,398 and the slope on hashrate is positive. The R-squared is roughly 0.299, meaning about 30% of the cross-sample variation in price is associated with variation in hashrate. The t-statistic on the hashrate coefficient is 27.9 and the corresponding p-value is on the order of 10⁻¹⁴³, so the association is not a statistical fluke.

At the same time, the regression diagnostics keep us honest. The Durbin–Watson statistic is basically zero, which tells us the residuals are highly autocorrelated. In plain language: there is a lot of serial dependence left over that this simple model does not try to account for. That is fine for this project, because our goal is not forecasting. The model is a rough lens on how much of the long-run price variation lines up with the long-run growth in network security.

Putting everything together, the findings look like this: Bitcoin’s financial valuation and its physical security layer clearly move together over multi-year horizons, but they do not move in lockstep. Hashrate climbs steadily; price moves in aggressive waves around that trend. The regression confirms that the link is statistically and economically meaningful, but also leaves plenty of room for the rest of the crypto circus—macro shocks, leverage, regulation, and narrative—to do its work on price.

## Future Work

This project is intentionally modest in its modeling ambitions. We collected two datasets, cleaned them carefully, and fit a straightforward regression. That is enough to say something concrete about how price and hashrate line up, but it also leaves a lot on the table. If we were to push this forward, there are several directions that feel natural.

One obvious extension is to move from levels to logs. Right now the regression is run on raw `price_btc` and `hashrate_btc`. That works mechanically, but it is numerically awkward, and it is not the language economists usually use. A log–log specification would let us talk about elasticities: if hashrate goes up by 1%, what is the associated percentage change in price, on average? It would also scale down the huge magnitudes in the hashrate series and likely produce a better-conditioned design matrix.

A second extension is to stop pretending that simple OLS on daily data fully captures the time-series structure. The Durbin–Watson statistic in our current model is essentially zero, which is a big warning sign that the residuals are autocorrelated. A more serious treatment would reach for vector autoregressions, error-correction models, or at least some kind of lag structure on both variables. That would open the door to asking more directional questions, like whether price tends to lead changes in hashrate or whether miners get ahead of market moves.

A third direction is to add more variables that represent other parts of the Bitcoin system. Difficulty adjustments, block reward halvings, transaction fees, stablecoin flows, and even rough measures of global risk sentiment could all play a role in explaining how price and hashrate move together. The current model effectively says, “nothing else matters,” which is obviously not true. A richer specification would not be as clean conceptually, but it would get closer to the real causal graph.

There is also room to enlarge the time window. Our sample stops at the beginning of 2023. Since then, we have seen higher interest rates, the slow normalization of the post-FTX landscape, and the early stages of spot ETF discussions. Extending the dataset to include those years would tell us whether the price–hashrate relationship has been stable across changing macro environments or whether it is regime-dependent.

On the engineering side, the workflow could be hardened even further. Right now the pipeline is scripted and checksummed, which is a good start. If we wanted to treat this as a real research asset, we could put the whole thing in a container, publish it to a long-term archive, and pin exact dependency versions. That would make it much easier for someone five years from now to reproduce the analysis even if the underlying APIs or Python ecosystem change.

Finally, the same general template could be applied outside of Bitcoin. The structure of the project is: pick a system where there is a market-facing variable and an infrastructure variable, collect both over time, and ask how they move together. Ethereum price versus gas usage, power prices versus system load in electricity markets, or GPU prices versus AI training demand would all fit into that mold. Bitcoin is a clean first case because the protocol is simple and the data are easy to get, but the broader idea is to treat financial and physical layers as parts of a single feedback mechanism rather than separate worlds.

## Reproducibility

1. Clone the GitHub repository to your local machine.
2. Create and activate a Python virtual environment.
3. Install the required dependencies and run the full pipeline:
   ```bash
   pip install -r requirements.txt
   python scripts/data_01.py
   python scripts/clean_integrate_02.py
   python scripts/analyze_03.py

## References

- Yahoo Finance API – BTC-USD historical price data  
- Blockchain.com API – Bitcoin network hashrate data  
- Python Software Foundation (Python 3.x)  
- Pandas documentation  
- Matplotlib documentation  
- Statsmodels documentation  


