from .db import get_db

from flask import render_template, Blueprint

bp = Blueprint('research', __name__)


@bp.route('/research', methods=('GET', 'POST'))
def get_papers():

    papers = []
    return render_template("research.html", papers=papers)
