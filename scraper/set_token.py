from Robinhood import Robinhood
import json

username = input('username: ')
password = input('password: ')

svc = Robinhood()
try:
    svc.login(username=username,password=password)
except:
    tfa_input = input('2fa int token: ')
    svc.login(username,password,tfa_input)

data={}
data['auth_token']=svc.auth_token
data['refresh_token']=svc.refresh_token

with open('.private','w') as outfile:
    json.dump(data,outfile)

