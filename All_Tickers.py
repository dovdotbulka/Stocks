import argparse
import bs4 as bs
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import pickle
import os
import requests

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.strip('\n')
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    print(tickers)        
    return tickers



def run(show, ticker, ticker_filename, verbose):

    if os.path.exists(ticker_filename):
        with open(ticker_filename, "rb") as f:
            tickers = pickle.load(f)
    else:
        tickers = []

    if show:
        print(tickers)
    else:
        if ticker not in tickers:
            tickers.append(ticker)

        with open(ticker_filename,"wb") as f:
            pickle.dump(tickers,f)
        
    return tickers	
	


    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--ticker", default='TSLA', help="stock ticker")
    parser.add_argument("-f", "--file", default='all_tickers.pickle', help="tickers file")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
    parser.add_argument('-s', '--show', action='store_true', help="shows all tickers")

    args = parser.parse_args()

    if args.verbosity > 1:
        print("--file ", args.file)
        print("--ticker ", args.ticker)
        print("--show ", args.show)
        
    tickers = run(args.show, args.ticker, args.file, args.verbosity)
    print(tickers)


if __name__ == "__main__":
    main()

