from flask import request, render_template, Blueprint, redirect, url_for
from models.etiqueta import Etiqueta
from models.pergunta import Pergunta
from models.blog import Blog

etiqueta_route = Blueprint('etiqueta', __name__, template_folder='../../front-end/templates')

# Rota para mostrar todas as etiquetas
@etiqueta_route.route('/etiqueta')
def etiqueta():
    etiquetas = Etiqueta.query.all()  # Pega todas as etiquetas
    return render_template('etiqueta.html', etiquetas=etiquetas)

# Rota para mostrar perguntas e blogs de uma etiqueta
@etiqueta_route.route('/etiqueta/<int:etiqueta_id>')
def mostrar_etiqueta(etiqueta_id):
    etiqueta = Etiqueta.query.get_or_404(etiqueta_id)
    
    # Aqui, você pode fazer a lógica para pegar as perguntas e blogs relacionadas a essa etiqueta
    perguntas = Pergunta.query.filter(Pergunta.etiquetas.any(codigo=etiqueta_id)).all()
    blogs = Blog.query.filter(Blog.etiquetas.any(codigo=etiqueta_id)).all()

    return render_template('detalhes_etiquetas.html', etiqueta=etiqueta, perguntas=perguntas, blogs=blogs)