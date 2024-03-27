import matplotlib.pyplot as plt 
import pandas as pd
from main import get_specific_coin_indepth_data, um_futures_client, symbol, interval   
from numpy import random

# Set Variables
investment = 1000
fee_per_transaction = 0.01

def strategy1(df):
    
    """Strategy 1"""
    
    print("################## strategy1 data ###############################")
    
    # Calculate the simple moving average (SMA)
    n_SMA = 200 # Adjust the period as needed
    df["SMA"] = df["Close"].rolling(window=n_SMA).mean()
    
    # Calculate Relative Strength Index (RSI)
    n_RSI = 14  # Adjust the period as needed
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=n_RSI).mean()
    avg_loss = loss.rolling(window=n_RSI).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Create a new column 'Signal' to store the buy and sell signals depending on the strategy
    df['Signal'] = df.apply(lambda x: 'Buy' if x['Close'] > x['SMA'] and x['RSI'] < 30
                            else 'Sell' if x['Close'] < x['SMA'] and x['RSI'] > 70 
                            else 'Hold', axis=1)
    
    # Store the data in a CSV file in Results folder
    df.to_csv('python_crypto_trading_bot/Results/1_strategy1.csv', sep=',', index=False, encoding='utf-8')
    
    return df
    
get_data = get_specific_coin_indepth_data(um_futures_client, symbol, interval)
get_stratety_results = strategy1(get_data)

def backtesting(df, investment=investment, fee_per_transaction=fee_per_transaction):
    
    """Backtesting."""
    
    # print("################## Backtesting data ###############################")
    
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
    
    # Filter only transaction rows (Buy or Sell)
    transactions = pd.DataFrame()
    transactions = df.loc[(df['Signal'] == 'Buy') | (df['Signal'] == 'Sell')]
    
    # drop rows with na 
    transactions = transactions.dropna()
    
    # add Columns to transactions Dataframe
    transactions['Profit/Loss_Investment'] = (100 / transactions['Close'] * transactions['Profit_per_Coin'])
    transactions['Profit/Loss_Investment_and_fees'] = transactions['Profit/Loss_Investment'] - abs(transactions['Profit/Loss_Investment']) * fee_per_transaction #(1 - fee_per_transaction))
    
    # Store the data in a CSV file in Results folder
    df.to_csv('python_crypto_trading_bot/Results/2_backtesting_strategy1.csv', sep=',', index=False, encoding='utf-8')
    transactions.to_csv('python_crypto_trading_bot/Results/3_backtesting_strategy1_transactions.csv', sep=',', index=False, encoding='utf-8')
    print(transactions)
    return df, transactions

def backtesting_visualization(df):
    
    """Backtesting Visualization."""
    
    # print("################## Backtesting Visualization data ###############################")
    
    # Plot the Close price, SMA, RSI, Buy and Sell signals
    fig, (ax1, ax2, rsi) = plt.subplots(3, sharex=True, figsize=(14, 7))
    
    # Plot Close price and SMA
    color = 'tab:blue'
    ax1.set_title('Close Price and SMA')
    ax1.set_ylabel('Price in USD', color=color)
    ax1.plot(df['Open_time'], df['Close'] , color=color, label='Close Price')
    ax1.plot(df['Open_time'], df['SMA'] , color='tab:orange', label='SMA')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc="upper right")
    
    # Plot Volume (ax2)
    df = df.sort_values(by='Volume')
    color = 'tab:orange'
    ax2.set_ylabel('Volume in Dollar', color=color) 
    ax2.bar(df['Open_time'], df['Volume'], align='edge', width=0.05, color=color, label='Volume in Dollars')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.yaxis.set_major_locator(plt.MaxNLocator(10)) 
    ax2.legend(loc="upper left")
    
    # Plot Number of trades (ax3) and merge them into Volume (ax2) plot
    df = df.sort_values(by='Number_of_trades')
    color = 'tab:green'
    ax3 = ax2.twinx()  # instantiate a second axes that shares the same x-axis
    ax3.set_title('Volume and Number of trades')
    ax3.set_ylabel('Number of trades', color=color)
    ax3.bar(df['Open_time'], df['Number_of_trades'], align='edge', width=0.05, color=color, label='Number of trades')
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.legend(loc="upper right")
    
    # Plot RSI Indicator and signals (Buy and Sell) as dots.
    df_signal = df.loc[(df['Signal'] == 'Buy') | (df['Signal'] == 'Sell')]
    df = df.sort_values(by='Open_time')
    df_signal = df_signal.sort_values(by='Open_time')
    color = 'tab:red'
    rsi.set_title('RSI Indicator')
    rsi.set_ylabel('RSI', color=color)
    rsi.plot(df['Open_time'], df['RSI'] , color=color, label='RSI')
    rsi.plot(df_signal['Open_time'], df_signal['RSI'], 'go', label='Buy/Sell', markersize=10)
    rsi.axhline(20, color='gray', linestyle='--')
    rsi.tick_params(axis='y', labelcolor=color)
    rsi.legend(loc="upper right")
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    #plt.show()
    
    # Save the plot as a file
    plt.savefig('python_crypto_trading_bot/Results/4_backtesting_strategy1_plot.png')

def backtesting_visualization_overview(df):
    
    """Backtesting Visualization overview."""
    
    #print("################## Backtesting Visualization overview ###############################")

    # Filter the DataFrame to only include the columns you're interested in
    df_filtered = df[['Open_time', 'Open', 'Profit/Loss_Investment', 'Profit/Loss_Investment_and_fees']]

    nbr_transactions = len(transactions)
    profit_cumulative = sum(transactions['Profit/Loss_Investment'])
    profit_cumulative_and_fees = sum(transactions['Profit/Loss_Investment_and_fees'])
        
    # Append additional information
    additional_info = pd.DataFrame({
        'Open_time': ['Number of transactions', 'Invested', 'Future_Coin', 'Profit/Loss', 'Profit/Loss after fees'],
        'Open': [nbr_transactions, investment, symbol, profit_cumulative, profit_cumulative_and_fees]
    })

    # Create a new figure
    fig, ax = plt.subplots(2, 1, figsize=(14, 7))
    
    # Add title to the plot
    plt.suptitle('Trading Strategy 1 Overview', fontsize=16)
    
    # Remove plot frame
    ax[0].axis('off')
    ax[1].axis('off')
    
    # Create a table for the DataFrame and save it as a .png file
    table_df = ax[0].table(cellText=df_filtered.values, colLabels=df_filtered.columns, cellLoc = 'center', loc='center')
    table_df.auto_set_font_size(False)
    table_df.set_fontsize(10)
    table_df.scale(1, 1.5)

    # Create a table for the additional information
    table_info = ax[1].table(cellText=additional_info.values, cellLoc = 'center', loc='center')
    table_info.auto_set_font_size(False)
    table_info.set_fontsize(10)
    table_info.scale(1, 1.5)

    # Save the table and additional information as a .png file
    plt.savefig('python_crypto_trading_bot/Results/5_backtesting_strategy_overview.png')
    
df, transactions = backtesting(get_stratety_results, investment, fee_per_transaction)
strategy_visualization = backtesting_visualization(df)
strategy_overview = backtesting_visualization_overview(transactions)
#backtest_strategy_visualization = backtesting_visualization(backtest_strategy)
