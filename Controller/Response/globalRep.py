from Controller.Function.globalFun import databaseIsDone
from flask import jsonify

def index():
    done = databaseIsDone()
    if done :
        return jsonify({'result': "Hello To Platform for learning through Multimedia ..."})
    else :
        return jsonify({'result': 'Database not Found ...'})