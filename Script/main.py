from apscheduler.schedulers.blocking import BlockingScheduler
from parametrization import *
from API_BinanceFutures_Test import *
from getData import *
from strategy import *
from strategy2 import *
from backtesting.backtesting import *
from backtesting.backtesting_visualization import *
from Execute_orders.execute_order import *
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
        """Backtesting environment."""
        print("############# Backtesting environment#############")
        
        # Get all futures crypt coin data
        #cryptodata = get_all_futures_cryptocoin_data(client_test)
        
        # Get specific futures crypt coin data
        #spec_cryptodata = get_specific_coin_data(client_test, params['symbol'])

        # Get specific futures crypto coin indepth data
        starttime_timestamp = int(time.mktime(datetime.datetime.strptime(params['startTime'], "%Y-%m-%d").timetuple()) * 1000)
        endtime_timestamp = int(time.mktime(datetime.datetime.strptime(params['endTime'], "%Y-%m-%d").timetuple()) * 1000)
        spec_cryptodata_indepth = get_specific_coin_indepth_data(client_test, params['symbol'], params['interval'], starttime_timestamp, endtime_timestamp, limit=1500)
        
        def apply_strategy2():
            
            ### Prepare data for strategy2
            evidence, labels = prepare_data(spec_cryptodata_indepth)
            print("#############Evidence and Labels#############")
            
            # use train_test_split function from sklearn and split data
            X_train, X_test, y_train, y_test = train_test_split(
                evidence, labels, test_size=TEST_SIZE, random_state=42
            )
            
            ### Train model
            # Convert 'Open_time' to number of milliseconds since the Unix epoch
            X_train['Open_time'] = (X_train['Open_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
            X_test['Open_time'] = (X_test['Open_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')

            # Drop label column to not biase the training model
            X_train = X_train.drop(columns=['label'])
            X_test = X_test.drop(columns=['label'])
            
            #X_train['Close_time'] = (X_train['Close_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
            #X_test['Close_time'] = (X_test['Close_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
            
            # Train model and save the model 11_1_strategy2_model.pkl
            model = train_model(X_train, y_train)    
            
            # Make predictions on the test set
            predictions = model.predict(X_test)

            ### Evaluate the prediction
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
            
            return model 
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
        # print("############# Binance Test environment #############")
        
        ########## load, prepare data and train model ###########
        ### Prepare data for strategy2
        TEST_SIZE = 0.01
        starttime_timestamp = int(time.mktime(datetime.datetime.strptime(params['startTime'], "%Y-%m-%d").timetuple()) * 1000)
        endtime_timestamp = int(time.mktime(datetime.datetime.strptime(params['endTime'], "%Y-%m-%d").timetuple()) * 1000)
        
        spec_cryptodata_indepth = get_specific_coin_indepth_data(client_test, params['symbol'], params['interval'], starttime_timestamp, endtime_timestamp, limit=1500)
        evidence, labels = prepare_data(spec_cryptodata_indepth)
        
        # use train_test_split function from sklearn and split data
        X_train, X_test, y_train, y_test = train_test_split(
            evidence, labels, test_size=TEST_SIZE, random_state=42
        )
        
        ######### Train model ###########
        # Convert 'Open_time' to number of milliseconds since the Unix epoch
        X_train['Open_time'] = (X_train['Open_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
        X_test['Open_time'] = (X_test['Open_time'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')

        # Drop label column to not biase the training model
        X_train = X_train.drop(columns=['label'])
        X_test = X_test.drop(columns=['label'])
        
        # Train model and save the model 11_1_strategy2_model.pkl
        model = train_model(X_train, y_train)    
                  
        ########## Set up trading job ###########
        # Get most recent specific futures crypto coin indepth data
        getlastdata = client_test.klines(symbol=params['symbol'], interval=params['interval'], limit=1)
        
        # Name the columns by definition. More information https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list --> Klines/Candlestick data
        column_names = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'] 
        
        # set the data into a pandas dataframe
        newest_spec_cryptodata_indepth = pd.DataFrame(getlastdata, columns=column_names)
            
        newest_spec_cryptodata_indepth['Open_time'] = pd.to_datetime(newest_spec_cryptodata_indepth['Open_time'], unit='ms')
        #print('############# Newest Spec Crypto Datafrae #############')
        #print(newest_spec_cryptodata_indepth)
        
        #### Make predictions based on the trained model
        # print('############# Prediction #############')
        
        # Convert 'Open_time' to number of milliseconds since the Unix epoch
        newest_spec_cryptodata_indepth = newest_spec_cryptodata_indepth.copy()
        newest_spec_cryptodata_indepth['Open_time'] = (pd.to_datetime(newest_spec_cryptodata_indepth['Open_time'], unit='ms') - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
        newest_spec_cryptodata_indepth['Close_time'] = (pd.to_datetime(newest_spec_cryptodata_indepth['Close_time'], unit='ms') - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
        
        # Make predictions on the test set
        prediction = model.predict(newest_spec_cryptodata_indepth)
                        
        # print('############# Prediction #############')
        print(prediction)
            
        ### Set up trading job based on the prediction
        if prediction == 1:
            # Set up trading job to BUY
            newest_spec_cryptodata_indepth['Signal'] = 'BUY'
            print('############# Buy Signal main #############')
            print(newest_spec_cryptodata_indepth)
            trading = trading_job(client_test, newest_spec_cryptodata_indepth, params['symbol'], params['investment'])
        elif prediction == 2:
            # Set up trading job to SELL
            print('############# Buy Signal main #############')
            print(newest_spec_cryptodata_indepth)
            newest_spec_cryptodata_indepth['Signal'] = 'SELL'
            trading = trading_job(client_test, newest_spec_cryptodata_indepth, params['symbol'], params['investment'])
        else:
            print('No buy or sell signal.')
            return 0
        # strategy = strategy1(df)

    else:
        print("No environment selected.")
    
if __name__ == "__main__":
    # main()
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', minutes=15, start_date='2024-05-04 08:46:00')  # Replace '2022-01-01 00:00:00' with your desired starting date and time
    print("start")
    scheduler.start()
    print("stop")
    