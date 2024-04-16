import logging
from binance.lib.utils import config_logging
import pandas as pd

# Print input data in pretty format
def pretty_print(data):
    for i in data:
        print(i)

# Get/Return Ticker Prices for all futures crypt coins
def get_all_futures_cryptocoin_data(client):
    
    """Fetch all crypto coin data."""
    # set logging level to debug
    config_logging(logging, logging.DEBUG)
    
    # get all ticker prices
    ticker_prices = client.ticker_price()
    logging.info(client.ticker_price())
    
    print('############ get_all_futures_cryptocoin_data ###################')
    show = pretty_print(ticker_prices)
    
    return ticker_prices
# a = get_all_futures_cryptocoin_data(um_futures_client)

# Get/Return Ticker Prices for ONE specific futures crypt coin
def get_specific_coin_data(client, symbol):
    
    """Fetch specific crypto coin data."""
    
    print('############ get spc coin data ###################')
    
    # set logging level to debug
    config_logging(logging, logging.DEBUG)
    spec_ticker_prices = client.ticker_price(symbol=symbol)
    print(spec_ticker_prices)
    
    # print(f'spce ticker price: {spec_ticker_prices}')
    logging.info(client.ticker_price(symbol))
    
    return spec_ticker_prices
#b = get_specific_coin_data(um_futures_client, symbol)

# Get/Return indepth data for one specific futures crypt coin
def get_specific_coin_indepth_data(client, symbol, interval, startTime, endTime):
    
    """ Fetch specific coin data in depth. """
    df = pd.DataFrame()

    # print("#############Specific Coin in depth data#############")
    
    # set logging level to debug
    config_logging(logging, logging.DEBUG)
    
    # get klines/candlestick data
    spec_future_coin_indepth_data = client.klines(symbol=symbol, interval=interval, startTime=startTime, endTime=endTime, limit=1500)
    
    # Name the columns by definition. More information https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list --> Klines/Candlestick data
    column_names = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'] 
    
    # set the data into a pandas dataframe
    df = pd.DataFrame(spec_future_coin_indepth_data, columns=column_names)
    
    # Optional: Convert data to float and datetime
    df["Close"] = df["Close"].astype(float)
    df['Volume'] = df['Volume'].astype(float) 
    df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
    #df['Close_time'] = pd.to_datetime(df['Close_time'], unit='ms')
    
    logging.info(client.klines(symbol, interval))
    
    # Optionally: Convert datetime to int
    """
    df['Open_time'] = pd.to_datetime(df['Open_time']).astype(int)
    df['Close_time'] = pd.to_datetime(df['Close_time']).astype(int)
    """
    
    return df