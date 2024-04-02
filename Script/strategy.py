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