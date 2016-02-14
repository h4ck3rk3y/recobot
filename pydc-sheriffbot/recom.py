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

from pymongo import MongoClient

client = MongoClient('10.42.0.16')
db = client.reco_bot_2


data = Data()
data.load('./dc_recom.dat', sep='::', format={'col':1,'row':0})


def similar(seq1, seq2):
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()>0.4

def similar_users(user, data=data):
    svd = SVD()
    svd.set_data(data)
    svd.compute(k=1000,min_values=0, pre_normalize=None, mean_center=False, post_normalize=True)
    return [i[0] for i in svd.similar(user)]



def recommended_files(user,data=data):
    svd = SVD()
    svd.set_data(data)
    svd.compute(k=1000,min_values=0, pre_normalize=None, mean_center=False, post_normalize=True)
    similar_users = [i[0] for i in svd.similar(user)]

    #recoms = svd.recommend(user,is_row=True,only_unknowns=True,n=50)
    predict_arr = []

    user_tths = db.user_list.find({'user':user})
    tths = [i['tth'] for i in user_tths]
    movie_names = []

    for i in similar_users[1:]:
        for j in db.user_list.find({'user':i}):
            if j['tth'] not in tths:
                movie_name = db.tths.find_one({'tth':j['tth']})['name']
                movie_names.append(movie_name)
                tths.append(j['tth'])
                predict_arr.append((movie_name,j['tth'],svd.predict(user,j['tth'])))

    predict_arr = sorted(predict_arr,key=lambda x:x[2],reverse=True)
    res = []
    c_res = 0
    for p in predict_arr:
        flag=0
        for r in res:
            if similar(p[0],r[0]):
                flag = 1
                break
        if flag == 0:
            res.append(p[1])
            c_res += 1
            if c_res > 10:
                return res

