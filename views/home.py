import os
import re

from flask import render_template, request
from flask.blueprints import Blueprint
from werkzeug import secure_filename

from config import UPLOAD_FOLDER

bp = Blueprint('home', __name__)
CH_REGEX = re.compile(r'[\u4e00-\u9fff]+')
ALLOWED_EXTENSIONS = frozenset(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@bp.route('/')
def home():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        if not CH_REGEX.search(filename):
            filename = secure_filename(filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return ''
