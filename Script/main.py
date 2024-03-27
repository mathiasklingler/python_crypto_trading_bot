import logging
import datetime
import pandas as pd
from binance.um_futures import UMFutures
from config import api_key, api_secret
from binance.lib.utils import config_logging
from binance.error import ClientError

# Set Variables

# api_key = '<api_key>'
# api_secret = '<api_secret>'
symbol = 'BTCUSDT'
interval = '15m'
um_futures_client = UMFutures()
df = pd.DataFrame()
startTime = '2019-09-12'
endTime = '2024-01-01'

def main():
    cryptodata = get_all_futures_cryptocoin_data()
    spec_cryptodata = get_specific_coin_data()
    print("#############Cryptodata#############")
    print(cryptodata)
    print(spec_cryptodata)
    return None


# get server time and convert it to a readable format
server_time = um_futures_client.time()
timestamp = server_time['serverTime'] / 1000
dt_object = datetime.datetime.fromtimestamp(timestamp)
print(dt_object)

# Connect to testnet future Binance, set client
um_futures_client = UMFutures(key=api_key, secret=api_secret, base_url="https://testnet.binancefuture.com")

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
    logging.info(um_futures_client.ticker_price("BTCUSDT"))
    
    print('############ get_all_futures_cryptocoin_data ###################')
    show = pretty_print(ticker_prices)
    
    return ticker_prices
# a = get_all_futures_cryptocoin_data(um_futures_client)

# Get/Return Ticker Prices for ONE specific futures crypt coin
def get_specific_coin_data(client, symbol):
    
    """Fetch specific crypto coin data."""
    
    # print('############ get spc coin data ###################')
    
    # set logging level to debug
    config_logging(logging, logging.DEBUG)
    spec_ticker_prices = client.ticker_price(symbol=symbol)
    
    # print(f'spce ticker price: {spec_ticker_prices}')
    logging.info(um_futures_client.ticker_price(symbol))
    
    return spec_ticker_prices
#b = get_specific_coin_data(um_futures_client, symbol)

# Get/Return indepth data for one specific futures crypt coin
def get_specific_coin_indepth_data(client, symbol, interval):
    
    """ Fetch specific coin data in depth. """
    
    # print("#############Specific Coin in depth data#############")
    
    # set logging level to debug
    config_logging(logging, logging.DEBUG)
    
    # get klines/candlestick data
    spec_future_coin_indepth_data = client.klines(symbol=symbol, interval=interval, startTime=startTime, endTime=endTime, limit=1500)
    
    # Name the columns by definition. More information https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list --> Klines/Candlestick data
    column_names = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'] 
    
    # set the data into a pandas dataframe
    df = pd.DataFrame(spec_future_coin_indepth_data, columns=column_names)
    df["Close"] = df["Close"].astype(float)
    df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
    df['Close_time'] = pd.to_datetime(df['Close_time'], unit='ms')
    logging.info(um_futures_client.klines(symbol, interval))
    
    return df
#coin_data_raw_depth = get_specific_coin_indepth_data(um_futures_client, symbol, interval)

# Execute an order    
def execute_order(um_futures_client, symbol):
    
    """Execute an order."""
    
    # Get the tick size and quantity for the symbol
    tickSize, minQty, maxQty = get_infos_execute_order(symbol)
    
    # Get ticker price
    price = get_specific_coin_data(um_futures_client, symbol)
    
    # print("#############Execute Order#############")
    
    # Start executing the order
    try:
        response = um_futures_client.new_order(
            symbol=symbol,
            side="SELL",
            type="LIMIT",
            quantity=minQty * 2,
            timeInForce="GTC",
            price=round(float(price['price']) / tickSize * tickSize, 2),
            )
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

def get_infos_execute_order(symbol):

    """Get the tick size and quantity for executing the order."""
    # Get symbol information
    symbols_info = um_futures_client.exchange_info() #.symbol_info("BTCUSDT")
    
    # Search for symbol
    for symbol_info in symbols_info["symbols"]:
        if symbol_info["symbol"] == symbol:
            
            # Read tick size, min quantity and max quantity
            print(symbol_info["filters"][0]["tickSize"])
            tickSize = float(symbol_info["filters"][0]["tickSize"])
            print(symbol_info["filters"][1]["minQty"])
            minQty = float(symbol_info["filters"][1]["minQty"])
            print(symbol_info["filters"][2]["maxQty"])
            maxQty = symbol_info["filters"][2]["maxQty"]
            break
    # Return tick size, min quantity and max quantity
    return tickSize, minQty, maxQty
# c = execute_order(um_futures_client, symbol)

# if __name__ == "__main__":Í
    # main()