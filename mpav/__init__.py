from flask import Flask
from flask import render_template
from . import db
import os


def create_app(test_config=None):
    # create and configure the app
    # - `instance_relative_config` - configuration files are relative to the instance folder (one level up)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # override this with a random value when deploying
        DATABASE=os.path.join(app.instance_path, 'mpav.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder (app.instance_path) exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        db_ = db.get_db()

        posts = db_.execute(
            "SELECT * FROM blogs"
        ).fetchall()

        print('len(blogs):', len(posts))

        return render_template("index.html", posts=posts)

    # Call the db initialisation code
    db.init_app(app)

    # Register projects blueprint
    from . import projects
    app.register_blueprint(projects.bp)

    # Register blogs blueprint
    from . import blogs
    app.register_blueprint(blogs.bp)

    # associate the endpoint name 'index' with the / url, so that url_for('index') or url_for('blog.index') both work
    app.add_url_rule('/', endpoint='index')

    # Register research blueprint
    from . import research
    app.register_blueprint(research.bp)

    return app

