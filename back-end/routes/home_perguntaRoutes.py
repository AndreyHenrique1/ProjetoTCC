from flask import request, render_template, Blueprint, redirect, url_for
from database.db import db
from models.pergunta import Pergunta
from models.categoria import Categoria
from models.etiqueta import Etiqueta  
from models.blog import Blog 
from models.perguntasEtiquetas import PerguntasEtiquetas
from sqlalchemy import func

homePergunta_route = Blueprint('home', __name__, template_folder='../../front-end/templates')

# Rota da página inicial
@homePergunta_route.route('/')
def homePergunta():
    categorias_selecionadas = request.args.getlist('categorias')
    etiquetas_selecionadas = request.args.get('etiquetas')
    ordenar_por = request.args.get('ordenar', 'recentes')
    page = request.args.get('page', 1, type=int)  
    
    perguntas = Pergunta.query

    # Filtra por categorias
    if categorias_selecionadas:
        perguntas = perguntas.filter(Pergunta.codCategoria.in_(categorias_selecionadas))

    # Filtra por etiquetas
    if etiquetas_selecionadas:
        etiquetas_selecionadas = [etiqueta.lstrip('#').strip() for etiqueta in etiquetas_selecionadas.split(',')]
        perguntas = perguntas.join(PerguntasEtiquetas).join(Etiqueta)\
                             .filter(Etiqueta.nome.in_(etiquetas_selecionadas))\
                             .group_by(Pergunta.codigo)\
                             .having(func.count(Etiqueta.codigo) == len(etiquetas_selecionadas))

    # Ordena as perguntas
    if ordenar_por == 'recentes':
        perguntas = perguntas.order_by(Pergunta.data_criacao.desc())
    elif ordenar_por == 'antigas':
        perguntas = perguntas.order_by(Pergunta.data_criacao.asc())

    # Paginando as perguntas
    per_page = 10  # Define quantas perguntas você quer por página
    perguntas_paginadas = perguntas.paginate(page=page, per_page=per_page, error_out=False)  

    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()

    return render_template('homePergunta.html', perguntas=perguntas_paginadas.items, 
                           pagination=perguntas_paginadas, categorias=categorias, etiquetas=etiquetas)
