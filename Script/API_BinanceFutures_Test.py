from binance.um_futures import UMFutures
import datetime
from config import api_key, api_secret

def client_test_binancefuture():
    # Connect to testnet future Binance, set client
    um_futures_client = UMFutures()

    # get server time and convert it to a readable format
    server_time = um_futures_client.time()
    timestamp = server_time['serverTime'] / 1000
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    print(f' servertime: {dt_object}')

    # Connect to testnet future Binance, set client
    um_futures_client = UMFutures(key=api_key, secret=api_secret, base_url="https://testnet.binancefuture.com")

    return um_futures_client

