import argparse
import datetime as dt
import pandas as pd
import pandas_datareader.data as web

def run(start, end, ticker, v):
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime.now()
    df = web.DataReader("TSLA", 'yahoo', start, end)
    print(df.head())
    df.to_csv('TSLA.csv')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", default='2015-01-01', help="starting date")
    parser.add_argument("-e", "--end", default='2020-12-31', help="end date")
    parser.add_argument("-t", "--ticker", default='TSLA', help="stock ticker")
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")
    
    
    args = parser.parse_args()

    if args.verbosity > 1:
        print("starting date={},  end date={}".format(args.start,args.end))
        if args.file != '':
            print("ticker file... ", args.file)
        
    run(args.start, args.end, args.ticker, args.verbosity)


if __name__ == "__main__":
    main()

