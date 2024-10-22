from flask import Flask, request, jsonify, render_template, Blueprint
from database.db import db
from models.pergunta import Pergunta
from models.categoria import Categoria
from models.Etiqueta import Etiqueta

home_route = Blueprint('home', __name__, template_folder='../../front-end/templates')

@home_route.route('/')
def home():
    categoria_id = request.args.get('categoria')
    categorias_selecionadas = request.args.getlist('categorias')
    etiquetas_selecionadas = request.args.getlist('etiquetas')  
    ordenar_por = request.args.get('ordenar')

    # Aplique filtros ao banco de dados com base nos parâmetros recebidos
    perguntas = Pergunta.query
    
    if categorias_selecionadas:
        perguntas = perguntas.filter(Pergunta.codCategoria.in_(categorias_selecionadas))

    
    if etiquetas_selecionadas:
        perguntas = perguntas.filter(Pergunta.etiquetas.any(Etiqueta.codigo.in_(etiquetas_selecionadas))) 
    
    if ordenar_por == 'recentes':
        perguntas = perguntas.order_by(Pergunta.data_criacao.desc())
    elif ordenar_por == 'antigas':
        perguntas = perguntas.order_by(Pergunta.data_criacao.asc())
    elif ordenar_por == 'sem_respostas':
        perguntas = perguntas.filter(Pergunta.respostas == 0)

    perguntas = perguntas.all()

    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()  

    return render_template('home.html', perguntas=perguntas, categorias=categorias, etiquetas=etiquetas)  

@home_route.route('/buscar_etiquetas')
def buscar_etiquetas():
    termo = request.args.get('termo', '')
    
    if termo:
        etiquetas = Etiqueta.query.filter(Etiqueta.nome.ilike(f'%{termo}%')).all()
    else:
        etiquetas = []

    etiquetas_json = [{'codigo': etiqueta.codigo, 'nome': etiqueta.nome} for etiqueta in etiquetas]
    return jsonify(etiquetas_json)

