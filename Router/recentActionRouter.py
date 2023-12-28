from flask import Blueprint
from Controller.Response.recentActionRep import getAction, updateGrade, rate

recentActionRouter = Blueprint('recentActionRouter', __name__)

recentActionRouter.route('/get', methods=['GET'])(getAction)
recentActionRouter.route('/rate', methods=['GET'])(rate)
recentActionRouter.route('/update', methods=['POST'])(updateGrade)