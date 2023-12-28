from flask import Flask, jsonify, request, current_app
from flask_mail import Mail, Message
from Controller.Function.userFun import createUser, loginUser, returnUser, resetPassword, editUser, getCodeVerify, storeCode, doneVerify

def signup():
    req = request.json
    print(req)
    result = createUser(req)
    print("result"+str(result))
    message = ''
    if result == -1 :
        message = "The email is already in use"
    elif result == -2 :
        message = "The account has not been created"
    else :
        message = "Done"
    return jsonify({
        'message': message,
        'result': str(result)
    })

def login():
    arg = request.args
    result = loginUser(arg)
    done = 'Done'
    if result == -1 :
        done = "False"
    return jsonify({
        'message': done ,
        'result': str(result)
    })

def getUser():
    arg = request.args
    result = returnUser(arg.get("id"))
    if result == -1 :
        return jsonify({"result" : "False"})
    else :
        return jsonify(result)

def resetPass():
    arg = request.json
    result = resetPassword(arg)
    if result == 1 :
        return jsonify({"result" : "Done"})
    else :
        return jsonify({"result" : "False"})

def updateUser():
    newInfo = request.json
    result = editUser(newInfo)
    if result == 1 :
        return jsonify({"result" : "Done"})
    else :
        return jsonify({"result" : "False"})

def getVerifyCode():
    mail = Mail(current_app)
    email = request.args["email"]
    print(email)
    code = getCodeVerify()
    msg = Message(
                'Your email confirmation code',
                sender ='eeducationalsystem@gmail.com',
                recipients = [email]
               )
    msg.html = """<html><body><div class="column">
        <b>To help us confirm your identity on our System , we need to verify your email address.
\nThis code can only be used once. \nIf you didn't request a code, please ignore this email. \nNever share this code with anyone else .\n</b>
        <b style="color:Gray;">Your email confirmation code :</b>
        <strong style="color:Tomato;font-size:25px;">{}</strong>
        </div></html></body>""".format(code)
    storeCode(code,email)
    mail.send(msg)
    return jsonify({"result" : "Done"})

def verify():
    arg = request.args
    result = doneVerify(arg)
    return jsonify({"result" : result})



