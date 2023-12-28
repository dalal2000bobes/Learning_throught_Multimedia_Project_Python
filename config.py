import pymongo as pm

client = pm.MongoClient("mongodb://localhost:27017/")
db = client["PlatformLearninigDatabase"]