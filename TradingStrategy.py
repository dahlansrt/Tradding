import DataLoading
import MACD
import RSI

f = open("idx.txt","r")
fw = open("macd_histogram.csv","w")
fw.write("Ticker,macd_histogram,rsi,volume\n")
for ticker in f.readlines():
    data = DataLoading.getData(ticker.strip(), 700)
    
    df = MACD.MACD(data)
    macd_histogram = df['MACD Histogram'].iat[-1]
        
    #if MACD > signal line  then buy else sell
    macd = df['MACD'].iat[-1] > df['Signal Line'].iat[-1]
        
    df = RSI.RSI(data)
    rsi = df['rsi'].iat[-1]
    volume = df['Volume'].iat[-1]
    
    if(macd_histogram <= 2 and rsi <= 30 and macd):
        fw.write(ticker.strip() + "," + str(macd_histogram) + "," + str(rsi) + "," + str(volume) + "\n")
        #print(ticker.strip(), " = ", macd_histogram)
f.close()
fw.close()