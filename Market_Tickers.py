import argparse
import bs4 as bs
import pickle
import os
import requests

### This is of little use currently as the Yahoo Finance API
### no longer works so we cannot go and programmatically get 
### historical quotes for a given list of tickers.
### For now, we are populating the quotes directory by
### downloading the CSV file manually, one at a time from
### Yahoo Finance.

# Build a collection of stock tickers.
# Allow the addition or removal of new stocks ticker as we go along.
# The very first time, start with a list of S&P 500 from Wikipedia.

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


# ticker_filename has the current list of stock tickers.
# If ticker_filename does not exist, assume this is first invocation.
#     Go get an initial list of S&P 500 stocks.   
# ticker is a stock we want to add to our universe.
def run(show, add_ticker, remove_ticker, ticker_filename, verbose):

    tickers = []
    if os.path.exists(ticker_filename):
        with open(ticker_filename, "rb") as f:
            tickers = pickle.load(f)
    else:
        if not show:
            tickers = init_sp500_tickers(ticker_filename)

    if add_ticker and add_ticker not in tickers:
        tickers.append(add_ticker)

    if remove_ticker and remove_ticker in tickers:
        tickers.remove(remove_ticker)

    with open(ticker_filename,"wb") as f:
        pickle.dump(tickers,f)
        
    return tickers	


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", help="add stock ticker")
    parser.add_argument("-r", "--remove", help="remove stock ticker")
    parser.add_argument("-f", "--file", default='all_tickers.pickle', help="tickers file")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
    parser.add_argument('-s', '--show', action='store_true', help="shows all tickers")

    args = parser.parse_args()

    if args.verbosity > 1:
        print("--file ", args.file)
        print("--add ", args.add)
        print("--remove ", args.remove)
        print("--show ", args.show)
        
    tickers = run(args.show, args.add, args.remove, args.file, args.verbosity)
    if args.show:
        print(tickers)


if __name__ == "__main__":
    main()

