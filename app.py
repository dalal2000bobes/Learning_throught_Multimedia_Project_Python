from flask import Flask, render_template, jsonify, request
import os
from Router import UserRouter, globalRouter, imageRouter, convertFileRouter, summaryRouter, recentActionRouter

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('Files\Images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER_TEMP = os.path.join('Files\Temp')
UPLOAD_FOLDER_WORD = os.path.join('Files\Word')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_WORD'] = UPLOAD_FOLDER_WORD
app.config['UPLOAD_FOLDER_TEMP'] = UPLOAD_FOLDER_TEMP
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'eeducationalsystem@gmail.com'
app.config['MAIL_PASSWORD'] = 'czpkzrsrvaabzqyx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.register_blueprint(UserRouter.userRouter, url_prefix='/users')
app.register_blueprint(imageRouter.imageRouter, url_prefix='/image')
app.register_blueprint(convertFileRouter.convertFileRouter, url_prefix='/convert/file')
app.register_blueprint(summaryRouter.summaryRouter, url_prefix='/summary')
app.register_blueprint(recentActionRouter.recentActionRouter, url_prefix='/action')
app.register_blueprint(globalRouter.globalRouter, url_prefix='/')

if __name__ == '__main__':
    app.debug = True

    app.run(host='0.0.0.0', debug=True)