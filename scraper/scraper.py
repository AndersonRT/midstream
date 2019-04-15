from Robinhood import Robinhood
import requests
import pandas as pd

import json
from itertools import zip_longest
import os
import time


instrument_base_url = 'https://api.robinhood.com/instruments/?cursor='
popularity_base_url = 'https://api.robinhood.com/instruments/popularity/?ids='

rh = Robinhood()
rh.login(os.environ['robinhood_username'], os.environ['robinhood_password'])

#instruments = rh.instruments('')
next_instruments_query = instrument_base_url

while next_instruments_query:

    response = requests.get(next_instruments_query,timeout=15)
    instruments = response.json()['results']
    next_instruments_query = response.json()['next']

    results = []

    print(next_instruments_query)

    curr_time = pd.Timestamp.now()
    symbol_dict = {rec['id']:rec['symbol'] for rec in instruments if rec['tradability']=='tradable'}
    for ids in zip_longest(*(iter(list(symbol_dict.keys())),) * 15):

        instrument_query_string = ','.join(filter(None,ids))
        popularity_url = popularity_base_url+instrument_query_string
        print(popularity_url)
        response = requests.get(popularity_url,timeout=15)
        response = response.json()['results']

        popularity_score = [res['num_open_positions'] for res in response]

        result = [{'ts':curr_time,'symbol':symbol_dict[id],'popularity':p} for id,p in zip(ids,popularity_score) ]
        results.extend(result)
        time.sleep(2.5)

    if results:
        df=pd.DataFrame(results)
        df = df[['ts','symbol','popularity']]

        if not os.path.isfile('./data/results.csv'):
            df.to_csv('./data/results.csv', header=True,index=False)
        else: # else it exists so append without writing the header
            df.to_csv('./data/results.csv', mode='a', header=False,index=False)


