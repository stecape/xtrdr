import pymongo
import json

dbAlive = False

with open("./server/vects.json", 'r') as f:
    vects = json.load(f)
    
#creazione connettore a database mongo, database e collezioni
while dbAlive == False:
    try:
        mongoclient = pymongo.MongoClient("mongodb://127.0.0.1:3001/")
        mongoclient.server_info()
        dbAlive = True
    except:
        print("MongoDB - Connection error... try again...")

HMIdb = mongoclient["meteor"]
SetCol = HMIdb["Set"]
ActCol = HMIdb["Act"]
LogicCol = HMIdb["Logic"]
ButtonCol = HMIdb["Button"]
AlarmCol = HMIdb["Alarm"]

#inizializzazione DB
if SetCol.count_documents({})==0:
    SetCol.insert_many(vects['set'])
if ActCol.count_documents({})==0:
    ActCol.insert_many(vects['act'])
if LogicCol.count_documents({})==0:
    LogicCol.insert_many(vects['logic'])
if ButtonCol.count_documents({})==0:
    ButtonCol.insert_many(vects['button'])
if AlarmCol.count_documents({})==0:
    AlarmCol.insert_many(vects['alarm'])
