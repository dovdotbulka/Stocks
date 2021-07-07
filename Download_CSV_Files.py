import argparse
import bs4 as bs
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import pickle
import os
import requests

### This is of little use currently as the Yahoo Finance API
### no longer works so we cannot go and programmatically get 
### historical quotes for a given list of tickers.
### For now, we are populating the quotes directory by
### downloading the CSV file manually, one at a time from
### Yahoo Finance.

# Build a collection of dataframes for stocks that we can slice and dice later.
# This will be the universe of our stocks. 
# Keep all dataframes in a separate directory.

def init_sp500_tickers(filename):
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.strip('\n')
        tickers.append(ticker)
        
    with open(filename,"wb") as f:
        pickle.dump(tickers,f)

    return tickers


def get_data_from_yahoo(tickers, first_day, last_day):

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime.strptime(first_day, "%Y-%m-%d")
    end = dt.datetime.strptime(last_day, "%Y-%m-%d")

    for ticker in tickers:
        print(ticker)
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            #print(df.head())
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))



# ticker_filename has a list of stocks we already have dataframes for.
# If ticker_filename does not exist, assume this is first invocation.
#     Go get an initial list of S&P 500 stocks.   
# ticker is a stock we want to add to our universe.
def run(ticker_filename, start_date, end_date, ticker , verbose):

    tickers = []

    # if a ticker was provided, this is the only one we want quotes for
    # otherwise, get quotes for all tickers in the file
    if ticker:
        tickers.append(ticker)
    else:
        if os.path.exists(ticker_filename):
            with open(ticker_filename, "rb") as f:
                tickers = pickle.load(f)

    get_data_from_yahoo(tickers, start_date, end_date)
        
    return tickers	


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default='all_tickers.pickle', help="tickers file")
    parser.add_argument('-s', '--start', default='2005-1-1', help="start date")
    parser.add_argument('-e', '--end', default='2020-12-31', help="start date")
    parser.add_argument('-t', '--ticker', help="get quotes for this ticker only")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")


    args = parser.parse_args()

    if args.verbosity > 1:
        print("--file ", args.file)
        print("--start ", args.start)
        print("--end ", args.end)
        print("--ticker ", args.ticker)
         
    tickers = run(args.file, args.start, args.end, args.ticker, args.verbosity)
    if args.verbosity > 2:
        print(kickers)

if __name__ == "__main__":
    main()

