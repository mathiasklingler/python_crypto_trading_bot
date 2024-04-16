import matplotlib.pyplot as plt 
import pandas as pd

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

def backtesting_visualization_overview(transactions, investment, symbol):
    
    """Backtesting Visualization overview."""
    
    #print("################## Backtesting Visualization overview ###############################")

    # Filter the DataFrame to only include the columns you're interested in
    df_filtered = transactions[['Open_time', 'Open', 'Profit/Loss_Investment', 'Profit/Loss_Investment_and_fees']]

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
    