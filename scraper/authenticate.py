from Robinhood import Robinhood
import json

def authenticate(bot):
    with open('.private') as json_file:
        data = json.load(json_file)
        bot.auth_token=data['auth_token']
        bot.refresh_token=data['refresh_token']
        bot.headers['Authorization']='Bearer '+data['auth_token']
    return bot
