import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

def prepare_data(df):
    """
    Prepare data according to the model requirements. 
    The prepared data are used to train the model.
    
    Paramtetrization:
    - Timeframe 1 day=24h=360frames with 15min interval. This defines how long in the furture you look to make a decision.
    - If there is a value that is 2% higher than the buying price, set 'Buy'
    - If there is a value that is 2% lower than the buying price, set 'Sell'
    - Otherwise 'hold'.

    Prepare the data to train the model and save it as 11_1_strategy2.csv file. 
    Set labels. 
    """
    
    print("################## Prepare data ###############################")
    
    ### Strategy Parameters ###
    
    # take_profit sets the Buy/Sell signal from the Close price. 
    # If you increase take_profit, it takes more time to get from the initial close price to the Buy/Sell signal price.
    # As a result, you will have less signals.
    take_profit = 2 # 2%
    # The timeframe defines how long you look into the future to make a decision.
    timeframe = 38
    
    # Initialize lists to store the 'Signal' values
    Signal_list = []
    
    # Iterate through the DataFrame and calculate 'Signal' values
    for index, row in df.iterrows():
        
        # Get the Close value from the current row
        close_value = row['Close']
        
        # Iterate through next rows in DataFrame and compare it with the current row.
        # Iterate only over the next X rows, where X = timeframe. Set this parameter wisely.
        for _, next_row in df.iloc[index+1:index+1+timeframe].iterrows():
            
            # If The Close value hits the buy OR the sell signal, 
            if next_row['Close'] >= (1 + take_profit / 100) * close_value or next_row['Close'] <= (1 - take_profit / 100) * close_value:
                
                # If the next row value is higher than the current row value, set 'Buy' signal
                # Signals: 0 = hold, 1 = buy, 2 = sell
                if next_row['Close'] >= close_value:
                    signal = 1
                    break
   
                # If the next row value is lower than the current row value, set 'Sell' signal
                else:
                    signal = 2
                    break

            # If we do not have a signal in the next rows (nbr. of rows is defined by timeframe variable), set 'Hold' signal
            else:
                signal = 0
        
        # Append the result to the list
        Signal_list.append(signal)

    # add Signals Column to Dataframe
    df['label'] = Signal_list

    # Reduce the DataFrame by the timeframe number at the end to avoid bias.
    # At the end there is not enough data, because remaining rows < timeframe
    df = df.iloc[:-timeframe]
    
    # Store the data in a CSV file in Results folder
    df.to_csv('python_crypto_trading_bot/Results/11_1_strategy2.csv', sep=',', index=False, encoding='utf-8')
    return df, df['label']

model = KNeighborsClassifier(n_neighbors=1)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    k_model = model.fit(evidence, labels)
    joblib.dump(k_model, 'python_crypto_trading_bot/Results/11_1_strategy2_model.pkl')
    return k_model

def evaluate(labels, predictions):
    """
    Compare the labels from the prepared dataset against the predicted labels,
    return sensitivity rates for each label.
    """
    print("############ evaluate ###############*")
    #print(f'lables from y_test sample: {labels}')
    #print(f'predictions made by the model: {predictions}')
    
    # set init values
    hold_label = 0
    hold_label_true_positive = 0
    buy_label = 0
    buy_label_true_positive = 0
    sell_label = 0
    sell_label_true_positive = 0
    
    # loop over labels and predictions and compare
    for label, prediction in zip(labels, predictions):
        
        # If label is 0 = hold signal
        if label == 0:
            # Increase the hold_label counter
            hold_label += 1
            
            # If the prediction is correct, increase the hold_label_true_positive counter
            if label == prediction:
                hold_label_true_positive += 1
        
        # If label is 1 = buy signal
        elif label == 1:
            # Increase the buy_label counter
            buy_label += 1
            
            # If the prediction is correct, increase the buy_label_true_positive counter
            if label == prediction:
                buy_label_true_positive += 1
        
        # If label is 1 = buy signal
        elif label == 2:
            # Increase the sell_label counter
            sell_label += 1
            
            # If the prediction is correct, increase the sell_label_true_positive counter
            if label == prediction:
                sell_label_true_positive += 1
        else:
            return NotImplementedError("Label is not 0, 1 or 2")
    print(f'hold_label: {hold_label}')
    print(f'hold_label_true_positive: {hold_label_true_positive}')
    print(f'buy_label: {buy_label}')
    print(f'buy_label_true_positive: {buy_label_true_positive}')
    print(f'sell_label: {sell_label}')
    print(f'sell_label_true_positive: {sell_label_true_positive}')
    if hold_label != 0:
        sensitivity_rate_hold = hold_label_true_positive/hold_label
    else:
        sensitivity_rate_hold = 0
    if buy_label != 0:
        sensitivity_rate_buy = buy_label_true_positive/buy_label
    else:
        sensitivity_rate_buy = 0
    if sell_label != 0:
        sensitivity_rate_sell = sell_label_true_positive/sell_label    
    else:
        sensitivity_rate_sell = 0
    return (sensitivity_rate_hold, sensitivity_rate_buy, sensitivity_rate_sell)