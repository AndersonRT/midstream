import dash
import dash_core_components as dcc
import dash_html_components as html

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
import time
from flask import request
import json
import redis
import requests as basic_requests

from server import app, server
cache = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)


import multiday_chart
import intraday_chart




from data_placeholder import df


header = html.Div([
    html.H2('Finance Explorer -- Placeholder',
            style={'display': 'inline',
                   'float': 'left',
                   'font-size': '2.65em',
                   'margin-left': '7px',
                   'font-weight': 'bolder',
                   'font-family': 'Product Sans',
                   'color': "rgba(117, 117, 117, 0.95)",
                   'margin-top': '20px',
                   'margin-bottom': '0'})])


stock_selector = dcc.Dropdown(
        id='stock-ticker-input',
        options=[{'label': s[0], 'value': str(s[1])}
                 for s in zip(df.Stock.unique(), df.Stock.unique())],
        value=['YHOO', 'GOOGL'],
        multi=True)

body = html.Div(html.Div(id='graphs'))

app.layout = html.Div([header, stock_selector, body])


def update_robinhood_markets():
    url = 'https://api.robinhood.com/markets'
    resp = basic_requests.get(url)
    if resp.status_code == 200:
        markets_data = dict(json.loads(resp.content.decode('utf-8')))['results']
        markets_data = {v['mic'].lower():v for v in markets_data}

        for k,v in markets_data.items():
            cache.hmset(k, v)

        event = {'last_updated':int(time.time()),
                 'keys': str([*markets_data])}
        cache.hmset('markets',event)
    return cache.exists('markets')


@server.route('/api/<path:path>', methods=['GET'])
def home(path):

    path = path.lower()

    if not cache.exists(path):
        state = None
        if path == 'markets':
            state = update_robinhood_markets()

        if not state:
            return "Error: thing doesn't exist"

    available_keys = cache.hget(path,'keys')
    return available_keys, 200


@server.route('/api/<path:path>/<path:subpath>', methods=['GET'])
def subhome(path, subpath):

    path = path.lower()
    subpath = subpath.lower()

    if not cache.exists(path):
        state = None
        if path == 'markets':
            state = update_robinhood_markets()

        if not state:
            return "Error: thing doesn't exist"

    if not cache.exists(subpath):
        return "Error: thing doesn't exist"

    record = cache.hgetall(subpath)
    return str(record), 200


