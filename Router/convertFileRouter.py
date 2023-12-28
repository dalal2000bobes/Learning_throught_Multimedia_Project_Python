from flask import Blueprint
from Controller.Response.convertFileRep import convertPdf, convertImage

convertFileRouter = Blueprint('convertFileRouter', __name__)

convertFileRouter.route('/pdf/to/text',methods=["POST"])(convertPdf)
convertFileRouter.route('/image/to/text',methods=["POST"])(convertImage)