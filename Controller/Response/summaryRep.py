from Controller.Function.summaryFun import getSummaryExtractive, abstractiveModelSummarizer
# , getSummaryAbstractive
from flask import jsonify, request, current_app
from Controller.Function.questionFun import getQuestion
from Controller.Function.convertFileFun import wordExam , wordSum
from Controller.Function.recentActionFun import createAction
from werkzeug.utils import secure_filename
import os

def summary():
    print("heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeey")
    req = request.json
    print("Hello to Summerization ...")
    text = req['text']
    summary1 = abstractiveModelSummarizer(text)
    summary2 = getSummaryExtractive(text)
    qs = getQuestion(text)
    date = req["date"].split(".")
    date = date[0]
    links = ""
    linke = ""
    data = {
        'abs': summary1,
        'ex': summary2,
        "q" : qs["testQuestion"],
        "wi" : qs["wi"],
        "qs" : qs["qs"],
        "date" : date,
        "type" : req["type"],}
    sumWord = wordSum(data)
    examWord = wordExam(data)
    # paths = os.path.join(current_app.config['UPLOAD_FOLDER'], sumWord)
    links = "http://"+request.host +'/image/image?path='+sumWord
    # pathe = os.path.join(current_app.config['UPLOAD_FOLDER'], examWord)
    linke = "http://"+request.host +'/image/image?path='+examWord
    data = {
        'abs': summary1,
        'ex': summary2,
        "q" : qs["testQuestion"],
        "wi" : qs["wi"],
        "qs" : qs["qs"],
        "date" : date,
        "type" : req["type"],
        "urlSum" : links,
        "urlExam" : linke}
    id = createAction(data,req["id"])
    return jsonify({
        "id" : id,
        'abs': summary1,
        'ex': summary2,
        "q" : qs["testQuestion"],
        "urlSum" : links,
        "urlExam" : linke
        })
