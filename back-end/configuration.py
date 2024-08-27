from routes.homeRoutes import home_route
from routes.cadastrarRoutes import cadastrar_route
from routes.loginRoutes import login_route
from routes.perguntaRoutes import pergunta_route
from database.db import db
from flask_login import LoginManager

def configure_all(app):
    configure_routes(app)
    configure_db(app)
    app.config['SECRET_KEY'] = 'dergvfgf1234'
    login_manager = LoginManager(app)
    return login_manager

def configure_routes(app):
    app.register_blueprint(home_route)
    app.register_blueprint(cadastrar_route)
    app.register_blueprint(login_route)
    app.register_blueprint(pergunta_route)

def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/projetotcc'
    db.init_app(app)
