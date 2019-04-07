from flask import Flask
from dash import Dash
import redis

server = Flask('myproject')
app = Dash(server=server)
db = redis.Redis('localhost') #connect to server

app.config['suppress_callback_exceptions']=True

# Append CSS
app.css.append_css({
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css'
})

# Append JS
app.scripts.append_script({
    'external_url': 'http://velometria.com/static/ga.js'
})
app.scripts.append_script({
    'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js'
})

