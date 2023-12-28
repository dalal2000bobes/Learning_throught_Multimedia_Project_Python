from flask import jsonify, request
from Controller.Function.recentActionFun import returnAction, updateResult, returnRate

def getAction():
    req = request.args
    data = returnAction(req["id"])
    return jsonify(data)

def updateGrade():
    req = request.json
    print(req)
    updateResult(req)
    return jsonify({"result" : "Done"})

def rate():
    arg = request.args
    data = returnRate(arg["id"])
    return jsonify(data)
