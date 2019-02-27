from mpav.db import get_db

from flask import (
    g, render_template, request, session, url_for, Blueprint
)
from werkzeug.exceptions import abort

bp = Blueprint('blogs', __name__)


@bp.route('/')
def get_blogs():

    db = get_db()

    blogs_ = db.execute(
        "SELECT * FROM blogs"
    ).fetchall()

    print('len(blogs):', len(blogs_))

    return render_template(url_for("index.html", posts=blogs_))
