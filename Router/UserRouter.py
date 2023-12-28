from flask import Blueprint
from Controller.Response.userRep import signup, login, getUser, resetPass, updateUser, getVerifyCode, verify

userRouter = Blueprint('userRouter', __name__)

userRouter.route('/signup', methods=['POST'])(signup)
userRouter.route('/login', methods=['GET'])(login)
userRouter.route('/user/get', methods=['GET'])(getUser)
userRouter.route('/reset/password', methods=['POST'])(resetPass)
userRouter.route('/update/user',methods=['POST'])(updateUser)
userRouter.route('/verify/email',methods=["GET"])(getVerifyCode)
userRouter.route('/done/verify',methods=["GET"])(verify)