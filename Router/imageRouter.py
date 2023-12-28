from flask import Blueprint
from Controller.Response.imageRep import uploadImage, downImage, uploadOnlyImage, downFile

imageRouter = Blueprint('imageRouter', __name__)

imageRouter.route('/upload/image', methods=['POST'])(uploadImage)
imageRouter.route('/upload/image/only', methods=['POST'])(uploadOnlyImage)
imageRouter.route('/images',methods=['GET'])(downImage)
imageRouter.route('/image',methods=['GET'])(downFile)