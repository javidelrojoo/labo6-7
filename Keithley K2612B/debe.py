# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from pymongo import MongoClient
from bson import ObjectId

uri = "mongodb+srv://lbt:lbt@memristores.zss81fa.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri, server_api=ServerApi('1'))

db = cluster["memristores"]

row = db["terminal"]

dispositivo = {"Par": "C5-C6", "Last": [[1,2,3],2,3], "Rest": "150"}

dst = row.insert_one(dispositivo)

myquery = {"Par": "C5-C6"}
# mydoc = row.find(myquery)
# for i in mydoc:
#     print(i)
    
# update_dispositivo = { "$set": { "Rest":np.random.rand() }}

# row.update_many(myquery, update_dispositivo)

mydoc = row.find()
for i in mydoc:
    print(i)
