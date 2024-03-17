from binance.um_futures import UMFutures
import pandas as pd
from config import api_key, api_secret

def main():

    cryptodata = get_all_cryptocoin_data()
    spec_cryptodata = get_specific_coin_data()
    print("#############Cryptodata#############")
    print(cryptodata)
    print(spec_cryptodata)
    return None

    
# test binance future account. More Information https://testnet.binancefuture.com/en/futures/BTCUSDT
# api_key = '189ba246fc281f6d25e3f4174afc18aae10bccaf918345bffd6def148ef9bcac'
# api_secret = 'cc7033a66c58e9d3ff97bc24b9a2750906079c0b69fd7c7c43c1fc1f3436e195'
#symbol = 'BTCUSD_PERP'
symbol = 'BTCUSDT'
interval = '15m'

cm_futures_client = UMFutures()

# HMAC Authentication
#client = Client(api_key, api_secret)
#print(client.account())
# Get account information
#print(cm_futures_client.account())

# get server time
print(cm_futures_client.time())

# Connect to testnet future Binance account
cm_futures_client = UMFutures(key=api_key, secret=api_secret, base_url="https://testnet.binancefuture.com")

# Testing/Development
coin_data_raw = cm_futures_client.ticker_price(symbol=symbol)
coin_data_raw2 = cm_futures_client.klines(symbol=symbol, interval=interval)
"""
print('############ coin data 2 ###################')
for i in coin_data_raw2:
    print(i)
#df = pd.DataFrame([vars(d) for d in asdf])
#print(f' cm_futures_client###################: {df}')
# Get account information
#print(cm_futures_client.account())
"""

# Print input data in pretty format
def pretty_print(data):
    """Display the data in a DataFrame."""
    for i in data:
        print(i)

# Get/Return Ticker Prices for all futures crypt coins
def get_all_futures_cryptocoin_data(client):
    """Fetch all crypto coin data."""
    ticker_prices = client.ticker_price()
    show = pretty_print(ticker_prices)
    return ticker_prices
a = get_all_futures_cryptocoin_data(cm_futures_client)



# Get/Return Ticker Prices for ONE specific futures crypt coin
def get_specific_coin_data(client, symbol):
    """Fetch specific data."""
    spec_ticker_prices = client.ticker_price(symbol=symbol)
    show_spec = pretty_print(spec_ticker_prices)
    return spec_ticker_prices
b = get_specific_coin_data(cm_futures_client, symbol)

# Get/Return indepth data for one specific futures crypt coin
def get_specific_coin_indepth_data(client, symbol, interval):
    # Fetch specific coin data in depth.
    spec_future_coin_indepth_data = client.klines(symbol=symbol, interval=interval)
    # Name the columns by definition. More information https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list --> Klines/Candlestick data
    column_names = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'] 
    df = pd.DataFrame(spec_future_coin_indepth_data, columns=column_names)
    df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
    df['Close_time'] = pd.to_datetime(df['Close_time'], unit='ms')
    print(df)
    return spec_future_coin_indepth_data

print("#############Specific Coin in depth data#############")
coin_data_raw_depth = get_specific_coin_indepth_data(cm_futures_client, symbol, interval)



"""def prepare_order(symbol, quantity, order_type=cm_futures_client.ORDER_TYPE_LIMIT, price=None):
    # Prepare an order
    order = {
        'symbol': symbol,
        'quantity': quantity,
        'type': order_type,
    }
    if price:
        order['price'] = price
    return order

def execute_order(order):
    # Execute an order.
    if order['type'] == cm_futures_client.ORDER_TYPE_LIMIT:
        result = client.order_limit_buy(**order)
    else:
        result = client.order_market_buy(**order)
    return result
"""

# if __name__ == "__main__":
    # main()