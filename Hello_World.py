import argparse
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import os

def ticker_universe(ticker_file, verbose):
	my_col = 'Universe'
	tickers = []
	if ticker_file != '':
		df = pd.read_csv(ticker_file)
		cols = df.columns.tolist()
		if my_col not in cols:
			print("ticker_universe()::{} column not found in {}".format(my_col, cols))
			return tickers
		col = df[my_col]
		col.dropna(inplace=True)

		tickers = col.tolist()
		if verbose > 1:
			print("ticker_universe()::column {}".format(col))
			print("ticker_universe()::{} stock tickers...{}".format(my_col, tickers))
		

def run(start, end, ticker, ticker_file, verbose):
	#ticker_universe(ticker_file, verbose)
	if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
		try:
			df = web.DataReader(ticker, 'yahoo', start, end)
		except Exception as e:
			print("Bad ticker..." + ticker)
			print(e)
			return

		print(df.head())
		df.to_csv('stock_dfs/{}.csv'.format(ticker))
	else:
		print('stock_dfs/{}.csv already exists'.format(ticker))

    

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--start", default='2001-01-01', help="starting date")
	parser.add_argument("-e", "--end", default='2021-05-01', help="end date")
	parser.add_argument("-t", "--ticker", default='TSLA', help="stock ticker")
	parser.add_argument("-f", "--file", default='', help="tickers file")
	parser.add_argument("-v", "--verbosity", action="count", default=0,
	                    help="increase output verbosity")
    
    
	args = parser.parse_args()

	if args.verbosity > 1:
		print("starting date={},  end date={}".format(args.start,args.end))
		if args.file != '':
			print("ticker file... ", args.file)
        
	run(args.start, args.end, args.ticker, args.file, args.verbosity)


if __name__ == "__main__":
	main()

