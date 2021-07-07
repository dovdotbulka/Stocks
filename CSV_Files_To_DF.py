import argparse
import pandas as pd
import pickle
import os

def run(subdir, outfile, verbose):

    files = os.listdir(subdir)
    main_df = pd.DataFrame()

    for f in files:
        if verbose > 0:
            print(f)
        
        df = pd.read_csv('stock_dfs/{}'.format(f))
        df.set_index('Date', inplace=True)

        ticker = os.path.splitext(f)[0]
        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if verbose > 1:
            print(df.head())
            if verbose > 2:
                print(df.tail())

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

    main_df.dropna(axis=1,inplace=True)

    if verbose > 0:
        print(main_df.head())
        if verbose > 1:
            print(main_df.tail())
    main_df.to_csv(outfile)



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default='stock_dfs', help="subdir keeping all csv files")
    parser.add_argument("-f", "--file", default='market_quotes.csv', help="historical quotes for all tickers")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")

    args = parser.parse_args()

    if args.verbosity > 0:
        print("--file ", args.file)
        print("--dir ", args.dir)
        
    run(args.dir, args.file, args.verbosity)


if __name__ == "__main__":
    main()

