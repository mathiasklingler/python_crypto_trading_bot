import pandas as pd

def backtesting(df, investment, fee_per_transaction):
    
    """Backtesting."""
    
    print("################## Backtesting data ###############################")
    
    # Initialize lists to store the 'Result' values
    TP_SP_values = []
    profit_ = []
    
    # Set Take Profit and Stop Loss
    take_profit = 2 # 2%
    stop_loss = 1 # 1%
    
    # delete DateTimeIndex, a new numeric index will be created automatically by pandas
    df = df.reset_index(drop=True)
    
    # drop rows with na 
    df = df.dropna()

    # Iterate through the DataFrame and calculate 'Result' values
    for index, row in df.iterrows():
        
        #select rows with buy signal
        if row['Signal'] == 'Buy':
            close_value = row['Close']
            higher_value = None
            lower_value = None
            profit_pos = None
            profit_neg = None
            
            # search for a value 1.02 (take_profit) times higher or 0.99 (stop_loss) times lower than the Close price. Add the values wich occurs first.
            for _, next_row in df.iloc[index+1:].iterrows():
                if next_row['Close'] >= (1 + take_profit / 100) * close_value:
                    # print("am in the higher buy value")
                    higher_value = next_row['Close']
                    profit_pos = higher_value - close_value
                    break
                elif next_row['Close'] < (1 - stop_loss / 100) * close_value:
                    # print("am in the lower buy value")
                    lower_value = next_row['Close']
                    profit_neg = lower_value - close_value
                    break
            result = higher_value if higher_value is not None else lower_value
            result_profit = profit_pos if profit_pos is not None else profit_neg
            TP_SP_values.append(result)
            profit_.append(result_profit)
        
        #select rows with sell signal
        elif row['Signal'] == 'Sell':
            close_value = row['Close']
            higher_value = None
            lower_value = None
            profit_pos = None
            profit_neg = None
            
            # search for a 0.98 (take_profit) times lower or 1.01 (stop_loss) higher than the Close price. Add the values wich occurs first.
            for _, next_row in df.iloc[index+1:].iterrows():
                if next_row['Close'] >= (1 + stop_loss / 100) * close_value:
                    higher_value = next_row['Close']
                    profit_neg = close_value - higher_value
                    break
                elif next_row['Close'] < (1 - take_profit / 100) * close_value:
                    lower_value = next_row['Close']
                    profit_pos = close_value - lower_value
                    break
            result = higher_value if higher_value is not None else lower_value
            result_profit = profit_pos if profit_pos is not None else profit_neg  
            TP_SP_values.append(result)
            profit_.append(result_profit)
        else:
            TP_SP_values.append(0)
            profit_.append(0)
        
     # add Columns to Dataframe
    df['TP/SP_values'] = TP_SP_values
    df['Profit_per_Coin'] = profit_
    
    
    """ Set up a summary table with the transactions only """
    # Filter only transaction rows (Buy or Sell)
    transactions = pd.DataFrame()
    transactions = df.loc[(df['Signal'] == 'Buy') | (df['Signal'] == 'Sell')]
    
    # drop rows with na 
    transactions = transactions.dropna()
    
    # add Columns to transactions Dataframe
    transactions['Profit/Loss_Investment'] = (investment / transactions['Close'] * transactions['Profit_per_Coin'])
    transactions['Profit/Loss_Investment_and_fees'] = transactions['Profit/Loss_Investment'] - abs(transactions['Profit/Loss_Investment']) * fee_per_transaction #(1 - fee_per_transaction))
    
    # Store the data in a CSV file in Results folder
    df.to_csv('python_crypto_trading_bot/Results/2_backtesting_strategy1.csv', sep=',', index=False, encoding='utf-8')
    transactions.to_csv('python_crypto_trading_bot/Results/3_backtesting_strategy1_transactions.csv', sep=',', index=False, encoding='utf-8')
    print(transactions)
    
    return df, transactions