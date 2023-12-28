from flask import Flask, jsonify, request, current_app, send_file, render_template, render_template_string
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from Controller.Function.imageFun import updataImage
import mammoth



def uploadImage():
    image = request.files['images']
    img_filename = secure_filename(str(datetime.now())+" "+image.filename)
    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename))
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename)
    id = request.args["id"]
    linkImage = "http://"+request.host +'/image/images?path='+path
    result = updataImage(id,linkImage)
    if result == 1 :
        return jsonify({"result" : "Done"})
    else :
        return jsonify({"result" : "False"})

def uploadOnlyImage():
    image = request.files['images']
    img_filename = secure_filename(str(datetime.now())+" "+image.filename)
    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename))
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], img_filename)
    linkImage = "http://"+request.host +'/image/images?path='+path
    return jsonify({"link" : linkImage})

def downImage():
    path = request.args["path"]
    print(path)
    print("Hello to view file")
    return send_file(path)

def downFile():
    path = request.args["path"]
    # id = request.args["id"]
    # if(id == "1"):
    print(path)
    print("Hello to view file")
    return send_file(path)
    # else:
    #     # html = convert_word_to_html(path)
    #     newPath = "http://"+request.host +'/image/images?path='+path+"&id=1"
    #     html = """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Word Document</title></head><body><iframe src="{}" width="100%" height="800px"></iframe></body></html>""".format(newPath)
    #     with open("html.html", 'w', encoding="utf-8") as f:
    #         f.write(html)
    #     return render_template_string(html)
