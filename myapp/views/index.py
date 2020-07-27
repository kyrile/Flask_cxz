from flask import render_template
from flask import Blueprint

blue = Blueprint('indexBlue', __name__)


@blue.route('/', methods=['GET'])
def index():
    return render_template('index.html')
