from flask import Flask, render_template
from config import Config
from extensions import db
from flask_migrate import Migrate
from routes import main
from models.user import User
from models.nota import Nota
from werkzeug.security import generate_password_hash, check_password_hash


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'mi_clave_secreta_super_segura'
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)




def register_resources(app):
    # Aqui se manda a registrar la ruta main
    app.register_blueprint(main)

if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000)