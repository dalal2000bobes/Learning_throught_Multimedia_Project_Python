from flask import Flask, jsonify, request, current_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from Controller.Function.convertFileFun import pdfToText, imageToText, wordExam, wordSum
from Controller.Function.summaryFun import getSummaryExtractive, abstractiveModelSummarizer
from Controller.Function.questionFun import getQuestion
from Controller.Function.recentActionFun import createAction
import pypandoc

def convertPdf():
    arg = request.args
    text = ""
    links = ""
    linke = ""
    file = request.files['files']
    text = pdfToText(file)
    text = text[10000:13000]
    summary1 = abstractiveModelSummarizer(text)
    summary2 = getSummaryExtractive(text)
    qs = getQuestion(text)
    date = arg["date"].split(".")
    date = date[0]
    data = {
        'abs': summary1,
        'ex': summary2,
        "q" : qs["testQuestion"],
        "wi" : qs["wi"],
        "qs" : qs["qs"],
        "date" : date,
        "type" : arg["type"],}
    sumWord = wordSum(data)
    examWord = wordExam(data)
    # paths = os.path.join(current_app.config['UPLOAD_FOLDER_WORD'], sumWord)
    links = "http://"+request.host +'/image/image?path='+sumWord
    # pathe = os.path.join(current_app.config['UPLOAD_FOLDER_WORD'], examWord)
    linke = "http://"+request.host +'/image/image?path='+examWord
    data = {
        'abs': summary1,
        'ex': summary2,
        "q" : qs["testQuestion"],
        "wi" : qs["wi"],
        "qs" : qs["qs"],
        "date" : date,
        "type" : arg["type"],
        "urlSum" : links,
        "urlExam" : linke}
    id = createAction(data,arg["id"])
    return jsonify({
        "id" : id,
        'abs': summary1,
        'ex': summary2,
        "q" : qs["testQuestion"],
        "urlSum" : links,
        "urlExam" : linke
        })
    # return jsonify({"result" : text})

def convertImage():
    print("Hello to Convert Image to Text ...")
    text = ""
    links = ""
    linke = ""
    arg = request.args
    image = request.files['images']
    image.save(os.path.join(current_app.config['UPLOAD_FOLDER_TEMP'], image.filename))
    img_filename = secure_filename(str(datetime.now())+" "+image.filename)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename)
    linkImage = "http://"+request.host +'/image/images?path='+path
    text = imageToText(image.filename,path)
    summary1 = abstractiveModelSummarizer(text)
    summary2 = getSummaryExtractive(text)
    qs = getQuestion(text)
    date = arg["date"].split(".")
    date = date[0]
    data = {
        'abs': summary1,
        'ex': summary2,
        "q" : qs["testQuestion"],
        "wi" : qs["wi"],
        "qs" : qs["qs"],
        "date" : date,
        "type" : arg["type"],}
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
        "type" : arg["type"],
        "urlSum" : links,
        "urlExam" : linke}
    id = createAction(data,arg["id"])
    return jsonify({
        "id" : id,
        'abs': summary1,
        'ex': summary2,
        "q" : qs["testQuestion"],
        "urlSum" : links,
        "urlExam" : linke
        })
    # return jsonify({
    #     "result" : text ,
    #     "image" : linkImage
    #     })

# def convertStringToWord(test):
#     with open('file.docx', 'w') as f:
#         f.write(test)

# def wordSum():

#     # convert
#     path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
#     link = "http://"+request.host +'/image/images?path='+path

#     # convert
#     path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
#     link = "http://"+request.host +'/image/images?path='+path
