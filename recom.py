import sys
import recsys.algorithm
recsys.algorithm.VERBOSE = True
from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.evaluation.prediction import RMSE, MAE
from recsys.datamodel.item import Item
import difflib
from scipy.linalg import norm
import divisi2
from recsys.algorithm.matrix import *
import unidecode

from pymongo import MongoClient

client = MongoClient('localhost')
db = client.reco_bot_2

def similar(seq1, seq2):
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()>0.4

def similar_users(user):
    if not type(user) is str:
        user = unidecode.unidecode(user)
    if db.done_users.find_one({'user':user})['recommended']==False:
        user_files = db.user_list.find({'user':user})
        f = open('./dc_recom.dat','a')
        for u in user_files:
            f.write(u['user'] + '::' + u['tth'])
            f.write('\n')
        f.close()
        db.done_users.update({'user': user}, {'user':user, 'recommended': True})

    data = Data()
    data.load('./dc_recom.dat', sep='::', format={'col':1,'row':0})
    svd = SVD()
    svd.set_data(data)
    svd.compute(k=1000,min_values=0, pre_normalize=None, mean_center=False, post_normalize=True)
    return [i[0] for i in svd.similar(user)]

def recommended_files(user):
    if not type(user) is str:
        user = unidecode.unidecode(user)
    if db.done_users.find_one({'user':user})['recommended']==False:
        user_files = db.user_list.find({'user':user})
        f = open('./dc_recom.dat','a')
        for u in user_files:
            f.write(u['user'] + '::' + u['tth'])
            f.write('\n')
        f.close()
        db.done_users.update({'user': user}, {'user':user, 'recommended': True})

    data = Data()
    data.load('./dc_recom.dat', sep='::', format={'col':1,'row':0})
    svd = SVD()
    svd.set_data(data)
    svd.compute(k=1000,min_values=0, pre_normalize=None, mean_center=False, post_normalize=True)
    similar_users = [i[0] for i in svd.similar(user,n=10)]

    newdata = Data()
    for i in range(0,len(similar_users),1):
        files = db.user_list.find({'user':similar_users[i]})
        for f in files:
            newdata.add_tuple((1.0,similar_users[i],f['tth']))
    svd.set_data(newdata)
    svd.compute(k=1000,min_values=0, pre_normalize=None, mean_center=False, post_normalize=True)
    recoms = svd.recommend(user,is_row=True,only_unknowns=True,n=100)

    res = []
    c_res = 0
    for p in recoms:
        flag=0
        for r in res:
            if similar(db.tths.find_one({'tth':p[0]})['name'],db.tths.find_one({'tth':r[0]})['name']):
                flag = 1
                break
        if flag == 0:
            res.append(p)
            c_res += 1
            if c_res > 10:
                k = []
                for i in res:
                    try:
                        j = 'magnet:?xt=urn:tree:tiger:'+i[0] + "&dn=" + unidecode.unidecode(db.tths.find_one({'tth': i[0]})['name'])
                    except:
                        j = 'magnet:?xt=urn:tree:tiger:'+i[0]
                    k.append(j)
                return k
    k = []
    for i in res:
        try:
            j = 'magnet:?xt=urn:tree:tiger:'+i[0] + "&dn=" + unidecode.unidecode(db.tths.find_one({'tth': i[0]})['name'])
        except:
            j = 'magnet:?xt=urn:tree:tiger:'+i[0]
        k.append(j)

    return k