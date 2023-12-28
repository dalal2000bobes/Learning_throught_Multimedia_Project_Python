from flask import Blueprint
from Controller.Response.globalRep import index

globalRouter = Blueprint('globalRouter', __name__)

globalRouter.route('/', methods=['GET'])(index)