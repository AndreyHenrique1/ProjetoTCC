from flask import request, render_template, Blueprint, redirect, url_for
from database.db import db
from models.pergunta import Pergunta
from models.categoria import Categoria
from models.etiqueta import Etiqueta  
from models.blog import Blog 
from models.perguntasEtiquetas import PerguntasEtiquetas
from sqlalchemy import func

homePergunta_route = Blueprint('home', __name__, template_folder='../../front-end/templates')

# Rota home das perguntas
@homePergunta_route.route('/')
def homePergunta():
    categorias_selecionadas = request.args.getlist('categorias')
    etiquetas_selecionadas = request.args.get('etiquetas')
    ordenar_por = request.args.get('ordenar', 'recentes')  
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
    elif ordenar_por == 'sem_respostas':
        perguntas = perguntas.filter(Pergunta.respostas == 0)

    perguntas = perguntas.all()
    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()  

    return render_template('homePergunta.html', perguntas=perguntas, categorias=categorias, etiquetas=etiquetas)
