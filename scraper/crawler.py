import json
from Robinhood import Robinhood
import pika
import pymongo
import time


class crawler(Robinhood):
    
    def authenticate(self):
        with open('.private') as json_file:
            data = json.load(json_file)
            self.auth_token=data['auth_token']
            self.refresh_token=data['refresh_token']
            self.headers['Authorization']='Bearer '+data['auth_token']

    def __init__(self):
        Robinhood.__init__(self)
        self.authenticate()


if __name__== "__main__":
    me = crawler()
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["popularity"]
    
    data = {'sym':'GE','ts':int(time.time()),'popularity':me.get_popularity('GE')}
    print(data)
    mycol.insert_one(data)

    print(me.get_popularity('GE'))
    
    mycol2 = mydb['instruments']
    mycol2.insert_many(me.instrument(''))

