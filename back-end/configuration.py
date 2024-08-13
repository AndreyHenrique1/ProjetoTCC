from routes.homeRoutes import home_route

def configure_all(app):
    configure_routes(app)
    # configure_db(app)
    # app.config['SECRET_KEY'] = 'dervfgvfgf1234'

def configure_routes(app):
    app.register_blueprint(home_route)

"""def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/farmacia'
"""

