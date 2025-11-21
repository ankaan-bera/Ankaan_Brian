

Timeline:

1. Writing code to extract the data for CryptoCurrency prices from CoinGecko API for our desired timeframe of 5 years. Status: Done
2. Writing code to extract the data for Hash Rates for different Cryptos from Glassnode API for our desired timeframe of 5 years. Status: Done
3. Making both of our datasets are stored in CSV format using Pandas. Status: Done
4. Going through the various coloumns for our two datasets, and selecting the coloumns that we need for our analysis. Status: Done
5. Going through our datasets, inspecting the rows, and cleaning out the data (removing Null Values, inconsistent data, missing timestamps, etc). Status: Done
6. Combine the timestamps, cyrpto prices, and hash rates into one CSV file. Status: Done
7. Create a Linear Regression for predicting Crypto Price based on hash rate. Status: To be done during Fall Break
8. Create a Chart showing the data we have collected, and plotting the Linear Regression. Status: To be done during Fall Break
9. Interpreting and Analyzing our result, and creating a final document and conclusion. Status: To be done during Fall Break


Changes to be made / Issues that were faced:

1. There are limitations for how far back in time the historical data from the APIs go.
2. There are limitations of how much data can be pulled from the APIs.
3. Timestamps from the two datasets may not be matching. We try to resolve it by looking at the individual data, and seeing if they match up logically.
4. We have tried changing which API we use to pull the data from, but the API that we currently have has proved be the best for the project.
5. We have tried out different time-periods, and we have found out that 5 year data is the best timeframe to analyze.
