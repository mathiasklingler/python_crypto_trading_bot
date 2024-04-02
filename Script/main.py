from parametrization import *
from API_BinanceFutures_Test import *
from getData import *
from strategy import *
from backtesting import *
from backtesting_visualization import *
from execute_order import *

def main():
    # Set up parameters
    params = parametrization
    # print(params['symbol'])
    
    # Set up client
    client_test = client_test_binancefuture()
    
    # Get all futures crypt coin data
    #cryptodata = get_all_futures_cryptocoin_data(client_test)
    
    # Get specific futures crypt coin data
    #spec_cryptodata = get_specific_coin_data(client_test, params['symbol'])

    # Get specific futures crypt coin indepth data
    spec_cryptodata_indepth = get_specific_coin_indepth_data(client_test, params['symbol'], params['interval'], params['startTime'], params['endTime'])
    print("#############spec Cryptodata indepth #############")
    print(spec_cryptodata_indepth)
    
    # Set up strategy
    strategy = strategy1(spec_cryptodata_indepth)
    
    # Set up backtesting
    #df, transactions = backtesting(strategy, params['investment'], params['fee_per_transaction'])
    
    # Set up backtesting visualization 
    #strategy_visualization = backtesting_visualization(df)
    #strategy_overview = backtesting_visualization_overview(transactions, params['investment'], params['symbol'])
    
    # Set up trading job
    today = datetime.today()
    start = datetime.today() - timedelta(days=200)
    df = get_specific_coin_indepth_data(client_test, params['symbol'], params['interval'], start, today)
    strategy = strategy1(spec_cryptodata_indepth)
    trading = trading_job(client_test, strategy, params['symbol'], params['investment'])
    
if __name__ == "__main__":
    main()
