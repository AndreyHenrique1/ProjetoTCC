from routes.homeRoutes import home_route
from routes.cadastrarRoutes import cadastrar_route
from routes.loginRoutes import login_route
from routes.perguntaRoutes import pergunta_route
from database.db import db
from extensions import login_manager
import os

def configure_all(app):
    configure_routes(app)
    configure_db(app)
    login_manager.init_app(app)
    app.config['SECRET_KEY'] = 'dergvfgf1234'
    UPLOAD_FOLDER = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para upload de arquivos

def configure_routes(app):
    app.register_blueprint(home_route)
    app.register_blueprint(cadastrar_route)
    app.register_blueprint(login_route)
    app.register_blueprint(pergunta_route)

def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3308/projetotcc'
    db.init_app(app)
