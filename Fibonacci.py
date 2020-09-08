import DataLoading
import pandas as pd

def f_retracement(df):
    price_min = df.Close.min()
    price_max = df.Close.max()
    
    # Fibonacci Levels considering original trend as upward move
    diff = price_max - price_min
    level1 = price_max - 0.236 * diff
    level2 = price_max - 0.382 * diff
    level3 = price_max - 0.618 * diff
    
    data = {'Level':[0, 0.236, 0.382, 0.618, 1], 'Price': [price_max, level1, level2, level3, price_min]}
    return pd.DataFrame(data)
    
data = DataLoading.getData("BBNI", 200)
df = f_retracement(data)
print(df)