from flask_frozen import Freezer
from mpav import create_app
from mpav import db
from mpav import projects

app = create_app()
freezer = Freezer(app)

if __name__ == '__main__':

    @freezer.register_generator(projects.show)
    def show():
        db_ = db.get_db()
        project_ids = db_.execute(
            'SELECT id FROM projects'
        ).fetchall()
        for id in project_ids:
            yield {'project-id': id}

    freezer.freeze()
