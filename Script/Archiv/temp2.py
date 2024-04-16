#!/usr/bin/env python
import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from config import api_key, api_secret
from binance.error import ClientError

um_futures_client = UMFutures(key=api_key, secret=api_secret, base_url="https://testnet.binancefuture.com")

def get_infos_execute_order(symbol):

    # Get the tick size for the symbol
    symbols_info = um_futures_client.exchange_info() #.symbol_info("BTCUSDT")
    # Iterate over the symbols
    for symbol_info in symbols_info["symbols"]:
        if symbol_info["symbol"] == symbol:
            print(symbol_info["filters"][0]["tickSize"])
            tickSize = symbol_info["filters"][0]["tickSize"]
            print(symbol_info["filters"][1]["minQty"])
            minQty = symbol_info["filters"][1]["minQty"]
            print(symbol_info["filters"][2]["maxQty"])
            maxQty = symbol_info["filters"][2]["maxQty"]
            break
    return tickSize, minQty, maxQty
    
d = get_infos_execute_order("BTCUSDT")