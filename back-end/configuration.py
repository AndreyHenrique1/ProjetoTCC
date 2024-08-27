from routes.homeRoutes import home_route
from routes.cadastrarRoutes import cadastrar_route
from routes.loginRoutes import login_route
from database.db import db

def configure_all(app):
    configure_routes(app)
    configure_db(app)
    app.config['SECRET_KEY'] = 'dergvfgf1234'

def configure_routes(app):
    app.register_blueprint(home_route)
    app.register_blueprint(cadastrar_route)
    app.register_blueprint(login_route)

def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3308/projetotcc'
    db.init_app(app)


