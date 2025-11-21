

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


In Depth Summary:
  1) We collaboratively mapped out our data lifecycle from how we want to acquire the data, to how we want to clean and model the data. Specifically, we want to focus on developing an iterative refinement lifecycle model. Due to the different time horizons we want to explore and continuous API calls, we want to continously improve our processes and consistently try to figure out where we can improve our process. In terms of the ethical side of our data collection, we did a deep dive into the rate limits and liscensing of the data we hope to use. Since it is mainly numeric data and no identifiable personal data is being extracted, we don't think there significant privacy concerns. The main ethical challenge of this project is the conclusion we determine from the data. We discussed how we have to be careful in the conclusions we reach from our data as we don't want to imply a correlation when none exists, especially since the pricing of crypto is rapidly changing and has real financial ramifications. In regard to storage, we are going to store our data in two separate formats (clean and raw). We believe that this decision will provide the most transparency, so any person viewing our pipeline can see what we viewed as relevant data and it gives them the option to include different data if they want reimplement our pipeline. Furthermore, we will have one file for our metadata and other documentation and we will have a single file for our scripts.
  2) In regard to the extraction of our data, we tested the API using some dummy code, just to see how much historical data we can get under rate limit restrictions as well as making sure our code will still process in a timely manner. After testing the APIs, we saved the neccessary data from the 5-year horizon and cleaned it so it will be ready for modeling. We are in the midst of exploring different statistical methods for exploring the data (currently landed on Linear Regression), but we plan to explore a wide variety of avenues before settling on a final method.

