# Stocks
Python code for stock market charts and simulations

$ python Hello_World.py --help

You provide a stock ticker, start data and end date, and the program
will fetch closing prices for that particular ticker and store them
in a csv file

Start with accepting one ticker from the CLI, pulling quotes for the given period.
produce a csv file and store it in a separate directory, stock_dfs/<ticker>.csv

Later, extend the program to read a list of tickers from elsewhere, maybe a tickers.csv
file with the first column called Universe, for the universe of stocks?

Develop the ability to pull up and join all the csv files in the stock_dfs dir to a single
data frame for all tickers. The tickers will be the columns and the rows are the dates.

1. Populate stock_dfs with ticker csv files. Done.
1a. Should I skip pulling quotes if the csv already exists? Yes. Done.
2. Accept a group of tickers from a file
3. Roll up all tickers to a single df
4. What dates should I go for? Twenty years? 2001-01-01 to now? Yes. Done.
5. Rename Hello_World.py to something more appropriate

