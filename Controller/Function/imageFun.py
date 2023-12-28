from config import db

def updataImage(id,path):
    db_table = db["Users"]
    upData = db_table.update_one({"_id" : id},{"$set" : {"image" : path}})
    print("Modified Count : " + str(upData.modified_count))
    if upData.modified_count == 1:
        return 1
    else :
        return -1