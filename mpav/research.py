from .db import get_db

from flask import render_template, Blueprint

bp = Blueprint('research', __name__)


@bp.route('/research', methods=('GET', 'POST'))
def get_papers():

    db = get_db()

    papers = db.execute(
        'SELECT * FROM papers'
    ).fetchall()

    return render_template("research.html", papers=papers)
#