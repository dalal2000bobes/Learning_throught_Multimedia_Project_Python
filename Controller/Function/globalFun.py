from config import client

def databaseIsDone():
    dbs = client.list_database_names()
    if "PlatformLearninigDatabase" in dbs :
        print("Database exist ...")
        return True
    else :
        print("Database isn't exist ...")
        return False