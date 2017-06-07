from flask import render_template
from flask.blueprints import Blueprint

bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    return render_template('index.html')
