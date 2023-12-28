from config import db
from bson.objectid import ObjectId
import random
from datetime import datetime

def createAction(data , id):
    db_table1 = db["Action"]
    db_table2 = db["Question"]
    db_table3 = db["Option"]
    currentId = str(ObjectId())
    action = {
    "_id" : currentId,
    "user_id" : id,
    "abs" : data["abs"],
    "ex" : data["ex"],
    "urlSum" : data["urlSum"],
    "urlExam" : data["urlExam"],
    "type" : data["type"],
    "date": data["date"],
    "result" : 0
    }
    res = db_table1.insert_one(action)
    for x in data["q"]:
        qId = str(ObjectId())
        q = {
            "_id" : qId,
            "actionId" : currentId,
            "text" : x["text"],
            "type" : "q"
        }
        res = db_table2.insert_one(q)
        for y in x["option"]:
            pId = str(ObjectId())
            p = {
                "_id" : pId,
                "questionId" : qId,
                "code" : y["code"],
                "text" : y["text"],
                "isCorrect" : y["isCorrect"]
            }
            res = db_table3.insert_one(p)
    return currentId

def updateResult(data):
    db_table = db["Action"]
    d = db_table.find_one({"_id" : data["id"]})
    print(d["result"])
    if d["result"] < data["result"]:
        upData = db_table.update_one({"_id" : data["id"]},{"$set" : {"result" : data["result"]}})

def returnAction(id):
    db_table1 = db["Action"]
    db_table2 = db["Question"]
    db_table3 = db["Option"]
    result = []
    act = db_table1.find({"user_id" : id})
    for x in act :
        # print(x)
        act1 = []
        qs = db_table2.find({"actionId" : x["_id"]})
        for y in qs:
            # print(y)
            op = db_table3.find({"questionId" : y["_id"]})
            listOp = []
            for z in op:
                # print(z)
                listOp.append(z)
            qs = {
                "text" : y["text"],
                "option" : listOp
            }
            act1.append(qs)
        result.append({
            "id" : x["_id"],
            "abs" : x["abs"],
            "ex" : x["ex"],
            "result" : x["result"],
            "date" : x["date"],
            "q" : act1,
            "urlSum" : x["urlSum"],
            "urlExam" : x["urlExam"],
            "type" : x["type"]
        })
    return result

def returnRate(id):
    db_table = db["Action"]
    allRate = 0
    rate1 = 0
    rate2 = 0
    rate3 = 0
    allRateN = 0
    rate1N = 0
    rate2N = 0
    rate3N = 0
    act = db_table.find({"user_id":id})
    for x in act :
        allRateN = allRateN +1
        allRate = allRate + x["result"]
    act1 = db_table.find({"user_id":id,"type":"1"})
    for y in act1 :
        rate1N = rate1N +1
        rate1 = rate1 + y["result"]
    act2 = db_table.find({"user_id":id,"type":"2"})
    for z in act2 :
        rate2N = rate2N +1
        rate2 = rate2 + z["result"]
    act3 = db_table.find({"user_id":id,"type":"3"})
    for w in act3 :
        rate3N = rate3N +1
        rate3 = rate3 + w["result"]
    r = 0
    r1 = 0
    r2 = 0
    r3 = 0
    if allRateN != 0 :
        r = int(allRate/allRateN)
    if rate1N != 0 :
        r1 = int(rate1/rate1N)
    if rate2N != 0 :
        r2 = int(rate2/rate2N)
    if rate3N != 0 :
        r3 = int(rate3/rate3N)
    return {
        "allRate" : r,
        "rate1" : r1,
        "rate2" : r2,
        "rate3" : r3,
    }






