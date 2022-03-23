import pandas as pd
import requests
import pandas as pd
import yfinance as yf
import sys
import requests
import io


start_date = sys.argv[1]
end_date = sys.argv[2]




url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
s = requests.get(url).content

companies = pd.read_csv(io.StringIO(s.decode('utf-8')))

symbols = companies['Symbol'].tolist()

#symbols = ['AAPL','AMZN','GOOGL','MSFT']

stock_final = pd.DataFrame()
# iterate over each symbol

# iterate over each symbol
for i in symbols:
    # print the symbol which is being downloaded
    #print( str(symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)  
    try:
        # download the stock price 
        stock = []
        stock = yf.download(i ,start=start_date, end=end_date, progress=False)
        print(stock)
        # append the individual stock prices 
        if len(stock) == 0:
            None
        else:
            stock['Name']=i
            stock_final = stock_final.append(stock,sort=False)
    except Exception:
        None

stock_final.to_csv(f'/opt/airflow/stocks_{start_date}.csv')