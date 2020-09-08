import DataLoading
import pandas as pd
import numpy as np

#Create a function to signal when to buy and sell an asset
def buy_sell(signal):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    for i in range(0,len(signal)):
        #if rsi < 30 then buy else sell
        if signal['rsi'][i] < 30:
            if flag != 1:
                sigPriceBuy.append(signal['Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        #elif signal['rsi'][i] > 70: 
        #    if flag != 0:
        #        sigPriceSell.append(signal['Close'][i])
        #        sigPriceBuy.append(np.nan)
        #        flag = 0
        #    else:
        #        sigPriceBuy.append(np.nan)
        #        sigPriceSell.append(np.nan)
        #elif signal['rsi'][i] > 30:
        #    flag = -1
        #    sigPriceBuy.append(np.nan)
        #    sigPriceSell.append(np.nan)
        else: #Handling nan values
            flag = -1
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy, sigPriceSell)
    
def RSI(df, period=14):
    chg = df['Close'].diff(1)
    gain = chg.mask(chg<0,0)
    df['gain'] = gain
    loss = chg.mask(chg>0,0)
    df['loss'] = loss
    avg_gain = gain.ewm(com = period - 1, min_periods = period).mean()
    avg_loss = loss.ewm(com = period - 1, min_periods = period).mean()
    df['avg_gain'] = avg_gain
    df['avg_loss'] = avg_loss
    rs = abs(avg_gain/avg_loss)
    rsi = 100-(100/(1+rs))
    df['rsi'] = rsi
    
    #Create buy and sell columns
    x = buy_sell(df)
    df['Buy_Signal_Price'] = x[0]
    df['Sell_Signal_Price'] = x[1]
    #return df.rsi.iat[-1]    
    return df
    
#data = DataLoading.getData("BBNI", 200)
#df = RSI(data)
#print(df[['Date', 'Close', 'rsi', 'Buy_Signal_Price', 'Sell_Signal_Price']].loc[(df['Buy_Signal_Price'].notnull() | df['Sell_Signal_Price'].notnull())])