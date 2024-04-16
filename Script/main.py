from parametrization import *
from API_BinanceFutures_Test import *
from getData import *
from strategy import *
from strategy2 import *
from backtesting.backtesting import *
from backtesting.backtesting_visualization import *
from execute_order import *
import datetime
import time
import pandas as pd

def main():
    # Set up parameters from parametrization.py
    params = parametrization
    TEST_SIZE = 0.3
    
    # Set up client
    client_test = client_test_binancefuture()
    
    if params['environment'] == 'backtesting':
        """Testnet environment."""
        print("#############Testnet environment#############")
        
        # Get all futures crypt coin data
        #cryptodata = get_all_futures_cryptocoin_data(client_test)
        
        # Get specific futures crypt coin data
        #spec_cryptodata = get_specific_coin_data(client_test, params['symbol'])

        # Get specific futures crypto coin indepth data
        starttime_timestamp = int(time.mktime(datetime.datetime.strptime(params['startTime'], "%Y-%m-%d").timetuple()) * 1000)
        endtime_timestamp = int(time.mktime(datetime.datetime.strptime(params['endTime'], "%Y-%m-%d").timetuple()) * 1000)

        spec_cryptodata_indepth = get_specific_coin_indepth_data(client_test, params['symbol'], params['interval'], starttime_timestamp, endtime_timestamp)
        print("#############spec Cryptodata indepth #############")
        
        def apply_strategy2():
            
            ### Prepare data for strategy2
            
            evidence, labels = prepare_data(spec_cryptodata_indepth)
            print("#############Evidence and Labels#############")
            
            # use train_test_split function from sklearn and split data
            X_train, X_test, y_train, y_test = train_test_split(
                evidence, labels, test_size=TEST_SIZE, random_state=42
            )
            
            ### Train model and make predictions
            
            # Convert 'Open_time' to number of milliseconds since the Unix epoch
            X_train['Open_time'] = (X_train['Open_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
            X_test['Open_time'] = (X_test['Open_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')

            #X_train['Close_time'] = (X_train['Close_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
            #X_test['Close_time'] = (X_test['Close_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
            
            # Train model
            model = train_model(X_train, y_train)    
            
            # Make predictions
            predictions = model.predict(X_test)

            ### Evaluate the model
            
            # Calculate the sensitivity rate
            sensitivity_rate_hold, sensitivity_rate_buy, sensitivity_rate_sell = evaluate(y_test, predictions)
            print(f"Correct overall: {(y_test == predictions).sum()}")
            print(f"Incorrect overall: {(y_test != predictions).sum()}")
            sensitivity_rate_overall = (y_test == predictions).sum() / len(predictions)
            print(f"sensitivity_rate_overall: {(100 * sensitivity_rate_overall):.2f}%" )
            print(f"sensitivity_rate_hold: {100 * sensitivity_rate_hold:.2f}")
            print(f"sensitivity_rate_buy: {100 * sensitivity_rate_buy:.2f}%")
            print(f"sensitivity_rate_sell: {100 * sensitivity_rate_sell:.2f}%")
            
            ### Set up backtesting
            
            # Merge predictions with the original dataset
            X_test.loc[:, 'Signals'] = predictions
            evidence = evidence.join(X_test['Signals'], how='left')
            
            # Fill NaN values with 0
            evidence['Signals'] = evidence['Signals'].fillna(0)
            
            # Set up backtesting
            df, transactions = backtesting(evidence, params['investment'], params['fee_per_transaction'])
            
            # Build and save figures
            strategy_visualization = backtesting_visualization(df)
            strategy_overview = backtesting_visualization_overview(transactions, params['investment'], params['symbol'])
        a = apply_strategy2()
                
        def apply_strategy1():
            # Set up backtesting
            # df, transactions = backtesting(strategy, params['investment'], params['fee_per_transaction'])
            
            # Set up backtesting visualization 
            #strategy_visualization = backtesting_visualization(df)
            #strategy_overview = backtesting_visualization_overview(transactions, params['investment'], params['symbol'])
            return None
        
    elif params['environment'] == 'testnet':    
        """ Binance Test environment."""
        print("############# Binance Test environment #############")
        
        # Set up trading job
        
        # Set start time today minus 200 days and end time today
        today = datetime.today()
        start = datetime.today() - timedelta(days=200)
        
        # load data
        df = get_specific_coin_indepth_data(client_test, params['symbol'], params['interval'], start, today)
        
        # Apply strategy and add Signal
        strategy = strategy1(df)
        
        # Set up trading job
        trading = trading_job(client_test, strategy, params['symbol'], params['investment'])
    else:
        print("No environment selected.")
    
if __name__ == "__main__":
    main()
