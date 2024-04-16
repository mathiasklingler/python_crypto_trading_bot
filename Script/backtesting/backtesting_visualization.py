import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np  

def backtesting_visualization(df):
    
    """Backtesting Visualization."""
    
    print("################## Backtesting Visualization data ###############################")
    
    # Convert columns to the correct data type
    df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')  # Convert Open_time to datetime
    df['Volume'] = df['Volume'].astype(float)  # Ensure 'Volume' is of type float
    
    # Create a new figure
    fig, (ax1, ax2, ax4) = plt.subplots(3, sharex=True, figsize=(18, 7))

    # Plot Close price and Signals
    df = df.sort_values(by='Open_time')
    df_signal_buy = df.loc[(df['Signals'] == 1)]
    df_signal_sell = df.loc[(df['Signals'] == 2)]
    color = 'tab:blue'
    ax1.set_title('Close Price and Signals')
    ax1.set_ylabel('Price in USD', color=color)
    ax1.plot(df['Open_time'], df['Close'], color=color, label='Close Price')
    ax1.plot(df_signal_buy['Open_time'], df_signal_buy['Close'], 'go', label='Buy', markersize=5)
    ax1.plot(df_signal_sell['Open_time'], df_signal_sell['Close'], 'go', label='Sell', markersize=5, color='red')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc="upper left")

    # Plot Volume (ax2)
    df = df.sort_values(by='Volume')
    color = 'tab:orange'
    ax2.set_ylabel('Volume', color=color) 
    ax2.bar(df['Open_time'], df['Volume'], align='edge', width=0.02, color=color, label='Volume in million Dollars')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc="upper left")
    # Set y-ticks
    # yticks = np.linspace(df['Volume'].min(), df['Volume'].max(), 5)  # Create 10 evenly spaced values between min and max of 'Volume'
    #ax2.set_yticks(yticks)
    """
    # Plot Number of trades (ax3) and merge them into Volume (ax2) plot
    ax3 = ax2.twinx()  # instantiate a second axes that shares the same x-axis
    df = df.sort_values(by='Number_of_trades')
    color = 'tab:green'
    ax3.set_title('Volume')
    ax3.set_ylabel('Number of trades', color=color)
    ax3.bar(df['Open_time'], df['Number_of_trades'], align='edge', width=0.05, color=color, label='Number of trades')
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.legend(loc="upper right")
    """
    
    # Plot Volume (ax2)
    df = df.sort_values(by='Volume')
    color = 'tab:green'
    ax4.set_title('Number of trades')
    ax4.set_ylabel('Number of trades', color=color) 
    ax4.bar(df['Open_time'], df['Number_of_trades'], align='edge', width=0.02, color=color, label='Number_of_trades')
    ax4.tick_params(axis='y', labelcolor=color)
    ax4.legend(loc="upper left")
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    
    # Save the plot as a file
    plt.savefig('python_crypto_trading_bot/Results/11_4_backtesting_strategy1_plot.png')
    # plt.show()
    
def backtesting_visualization_overview(transactions, investment, symbol):
    
    """Backtesting Visualization overview."""
    
    #print("################## Backtesting Visualization overview ###############################")

    # Filter the DataFrame to only include the columns you're interested in
    transactions['Open_time'] = pd.to_datetime(transactions['Open_time'], unit='ms')  # Convert Open_time to datetime
    transactions.sort_values(by='Open_time', inplace=True)
    
    df_filtered = transactions[['Open_time', 'Open', 'Profit/Loss_Investment', 'Profit/Loss_Investment_and_fees']]
    df_filtered = df_filtered.sort_values(by='Open_time')
    
    nbr_transactions = len(transactions)
    profit_cumulative = sum(transactions['Profit/Loss_Investment'])
    profit_cumulative_and_fees = sum(transactions['Profit/Loss_Investment_and_fees'])
        
    # Append additional information
    additional_info = pd.DataFrame({
        'Open_time': ['Number of transactions', 'Invested', 'Future_Coin', 'Profit/Loss', 'Profit/Loss after fees'],
        'Open': [nbr_transactions, investment, symbol, profit_cumulative, profit_cumulative_and_fees]
    })

    # Create a new figure
    fig, ax = plt.subplots(2, 1, figsize=(10, 50))
    
    # Add title to the plot
    plt.suptitle('Trading Strategy 1 Overview', fontsize=16)
    
    # Remove plot frame
    ax[0].axis('off')
    ax[1].axis('off')
    
    # Create a table for all Transactions and save it as a .png file
    # ax[0].set_title('Transactions', pad=20)
    table_df = ax[0].table(cellText=df_filtered.values, colLabels=df_filtered.columns, cellLoc = 'center', loc='center')
    # table_df.auto_set_font_size(False)
    table_df.set_fontsize(10)
    table_df.scale(1, 1.5)
    # ax[0].axis('off')
    
    # Create a table for the additional information
    table_info = ax[1].table(cellText=additional_info.values, cellLoc = 'center', loc='center')
    # table_info.auto_set_font_size(False)
    table_info.set_fontsize(10)
    table_info.scale(1, 1.5)
    # ax[1].axis('off')
    ax[1].set_title('Additional Information', pad=20)

    fig.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    
    # Save the table and additional information as a .png file
    plt.savefig('python_crypto_trading_bot/Results/11_5_backtesting_strategy_overview.png')
    # plt.show()