from flask import Blueprint
from Controller.Response.summaryRep import summary

summaryRouter = Blueprint('summaryRouter', __name__)

summaryRouter.route('/', methods=['POST'])(summary)