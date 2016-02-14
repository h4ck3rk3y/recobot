import sys
from pymongo import MongoClient

client = MongoClient('10.42.0.16')
db = client.reco_bot_2

def dat_build():    
    g = open('dc_recom.dat','wb')
    c = 0
    for i in db.user_list.find():
        try:
            g.write(i['user'] + '::' + i['tth'])
            g.write('\n')
            c+=1
        except:
            pass
    

if __name__ == '__main__':
    dat_build()
