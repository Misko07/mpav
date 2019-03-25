from flask_frozen import Freezer
from mpav import create_app
from mpav import projects

app = create_app()
freezer = Freezer(app)

if __name__ == '__main__':

    @freezer.register_generator
    def show():
        print("%%")
        projects.project_generator()

    freezer.freeze()
