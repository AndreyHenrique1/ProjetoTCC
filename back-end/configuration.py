from routes.home_perguntaRoutes import homePergunta_route
from routes.cadastrarRoutes import cadastrar_route
from routes.loginRoutes import login_route
from routes.perguntaRoutes import pergunta_route
from routes.blogRoutes import blog_route
from routes.usuarioRoutes import usuario_route
from routes.notificacaoRoutes import notificacao_route
from routes.denunciaRoutes import denuncia_route
from routes.ajudaRoutes import ajuda_route
from routes.etiquetasRoutes import etiqueta_route
from database.db import db
from extensions import login_manager
import cloudinary
import cloudinary.uploader
import cloudinary.api

def configure_all(app):
    configure_routes(app)
    configure_db(app)
    login_manager.init_app(app)
    configure_cloudinary()
    app.config['SECRET_KEY'] = 'dergvfgf1234'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def configure_routes(app):
    app.register_blueprint(homePergunta_route)
    app.register_blueprint(cadastrar_route)
    app.register_blueprint(login_route)
    app.register_blueprint(pergunta_route)
    app.register_blueprint(usuario_route)
    app.register_blueprint(blog_route)
    app.register_blueprint(notificacao_route)
    app.register_blueprint(denuncia_route)
    app.register_blueprint(etiqueta_route)
    app.register_blueprint(ajuda_route)
    
def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3308/projetotcc'
    db.init_app(app)

def configure_cloudinary():
    cloudinary.config(
        cloud_name="derfgx6ho",
        api_key="835891168484419",
        api_secret="ar1Qw_aDhS4BtLyRHwLEgupqy2Y"
    )