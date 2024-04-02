from getData import *
from binance.error import ClientError
from datetime import datetime, timedelta

def trading_job(client, df, symbol, investment_amount):
    
    """Trading job."""
    
    print("#############Trading Job#############")
    # Filter only last record
    df_lastrecord = df.iloc[-1]
    if df_lastrecord.Signal == 'Hold':
        print('Buy Signal. Execute order: ')
        print("Datum: ", datetime.today())
        order = execute_order(client, symbol, 'BUY', investment_amount, df_lastrecord['Close'])
        #get_symbol_infos(client, symbol)
        print(order)
    elif df_lastrecord.Signal == 'Sell':
        print('sell: ')
        print("Datum: ", datetime.today())
        print(df_lastrecord)
    else:
        print('no buy or sell signal.')
        print("Datum: ", datetime.today())
        print(df_lastrecord)
        return 0

# Execute an order    
def execute_order(client, symbol, side, quantity, price):
    
    """Execute an order."""
    
    # Get the tick size and quantity for the symbol
    tickSize, minQty, maxQty = get_symbol_infos(client, symbol)
    
    # Get ticker price
    ### price = get_specific_coin_data(client, symbol)
    
    # print("#############Execute Order#############")
    
    # Start executing the order
    try:
        response = client.new_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=minQty * 2,
            timeInForce="GTC",
            price=round(float(price) / tickSize * tickSize, 2),
            )
        logging.info(response)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

def get_symbol_infos(client, symbol):

    """Get the tick size and quantity for executing the order."""
    # Get symbol information
    symbols_info = client.exchange_info() #.symbol_info("BTCUSDT")
    
    # Search for symbol
    for symbol_info in symbols_info["symbols"]:
        if symbol_info["symbol"] == symbol:
            
            # Read tick size, min quantity and max quantity
            
            # print("tickSize: ")
            # print(symbol_info["filters"][0]["tickSize"])
            tickSize = float(symbol_info["filters"][0]["tickSize"])
            
            # print("minQty: ")
            # print(symbol_info["filters"][1]["minQty"])
            minQty = float(symbol_info["filters"][1]["minQty"])
            
            #print("maxQty: ")
            #print(symbol_info["filters"][2]["maxQty"])
            maxQty = symbol_info["filters"][2]["maxQty"]
            break
    # Return tick size, min quantity and max quantity
    return tickSize, minQty, maxQty