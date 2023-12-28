from config import db
from bson.objectid import ObjectId
import random

def createUser(req):
    db_table = db["Users"]
    user = {
    "_id" : str(ObjectId()),
    "firstName" : req["firstName"],
    "lastName" : req["lastName"],
    "email" : req["email"],
    "password" : req["password"],
    "latePosition" : float(req["latePosition"]),
    "longPosition" : float(req["longPosition"]),
    "token" : req["token"],
    "image" : req["image"],
    "type" : req["type"]
    # "lastUpdate": ""
    }
    isCreate = emailExist(user["email"])
    if isCreate == -1 :
        res = db_table.insert_one(user)
        print("Insert Data Result is:\n" + str(res.inserted_id))
        if not res :
            return -2
        return res.inserted_id
    else :
        return -1

def emailExist(email):
    db_table = db["Users"]
    data = db_table.find_one({"email" : email})
    if not data :
        return -1
    else :
        return data

def loginUser(arg):
    db_table = db["Users"]
    data = db_table.find_one({
        "email" : arg.get("email"),
        "password" : arg.get("password")
        })
    if not data :
        return -1
    else :
        return data["_id"]

def returnUser(id):
    db_table = db["Users"]
    data = db_table.find_one({"_id" : id})
    if not data :
        return -1
    else :
        return data

def resetPassword(arg):
    db_table = db["Users"]
    upData = db_table.update_one({"email" : arg["email"]},{"$set" : {"password" : arg["password"]}})
    print("Modified Count : " + str(upData.modified_count))
    return upData.modified_count

def editUser(req):
    db_table = db["Users"]
    user = {
    "firstName" : req["firstName"],
    "lastName" : req["lastName"],
    "email" : req["email"],
    "latePosition" : float(req["latePosition"]),
    "longPosition" : float(req["longPosition"]),
    "token" : req["token"],
    "type" : req["type"]
    }
    upData = db_table.update_one({"_id" : req["id"]},{"$set" : user})
    print("Modified Count : " + str(upData.modified_count))
    return upData.modified_count

def getCodeVerify():
    code= ""
    str="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefjhigklmnopqrstuvwxyz"
    for i in range(10):
        index=random.randrange(0,str.__len__())
        code+=str[index]
    return code

def storeCode(code,email):
    db_table = db["VerifyEmail"]
    verify = {
        "_id" : str(ObjectId()),
        "email" : email,
        "code" : code
    }
    data = db_table.insert_one(verify)
    print(data.inserted_id)
    if not data : 
        return False
    else :
        return True

def doneVerify(arg):
    db_table = db["VerifyEmail"]
    data = db_table.find_one({"email" : arg["email"] , "code" : arg["code"]})
    if not data :
        return False
    else :
        db_table.delete_many({"email" : arg["email"]})
        return True