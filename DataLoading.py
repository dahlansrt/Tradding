import requests
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
import pandas as pd

def getData(ticker, delta=60):
    try:
        # current date and time
        _from = (datetime.now() - timedelta(delta))
        _to = datetime.now()

        _from_timestamp = int(datetime.timestamp(_from)*1000)
        _to_timestamp = int(datetime.timestamp(_to)*1000)

        url = "http://SET_YOUR_URL/GetOHLCDaily"

        payload = "{{\"stockId\":\"{0}\",\"from\":\"\\/Date({1}+0700)\\/\",\"to\":\"\\/Date({2}+0700)\\/\"}}".format(ticker, str(_from_timestamp), str(_to_timestamp))
        #print(payload)

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        
        bars = response.json()['Bars']
        if not bars:
            return
        #print(type(bars))

        stock = pd.DataFrame(bars)
        stock['Stamp'] = stock['Stamp'].str[6:16]
        stock['Stamp'] = stock['Stamp'].astype(int)
        stock['Date'] = stock['Stamp'].apply(datetime.fromtimestamp)
        stock.set_index('Date')
        stock.drop('Stamp', axis=1, inplace=True)
        #print(stock)

        return stock

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6


#print(getData("BBCA"))