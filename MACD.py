import DataLoading
import pandas as pd
import numpy as np

#Create a function to signal when to buy and sell an asset
def buy_sell(signal):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    for i in range(0,len(signal)):
        #if MACD > signal line  then buy else sell
        if signal['MACD'][i] > signal['Signal Line'][i]:
            if flag != 1:
                sigPriceBuy.append(signal['Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif signal['MACD'][i] < signal['Signal Line'][i]: 
            if flag != 0:
                sigPriceSell.append(signal['Close'][i])
                sigPriceBuy.append(np.nan)
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else: #Handling nan values
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy, sigPriceSell)
  
def MACD(df):
    #Calculate the MACD and Signal Line indicators
    #Calculate the Short Term Exponential Moving Average
    ShortEMA = df.Close.ewm(span=12, adjust=False).mean() #AKA Fast moving average
    #Calculate the Long Term Exponential Moving Average
    LongEMA = df.Close.ewm(span=26, adjust=False).mean() #AKA Slow moving average
    #Calculate the Moving Average Convergence/Divergence (MACD)
    MACD = ShortEMA - LongEMA
    #Calcualte the signal line
    signal = MACD.ewm(span=9, adjust=False).mean()
    
    #Create new columns for the data frame 
    df['MACD'] = MACD
    df['Signal Line'] = signal
    df['MACD Histogram'] = df['MACD'] - df['Signal Line']
    
    #Create buy and sell columns
    x = buy_sell(df)
    df['Buy_Signal_Price'] = x[0]
    df['Sell_Signal_Price'] = x[1]
    
    return df


#data = DataLoading.getData("BBNI", 200)
#df = MACD(data)
#print(df.loc[(df['Buy_Signal_Price'].notnull() | df['Sell_Signal_Price'].notnull())])