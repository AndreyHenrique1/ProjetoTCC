from flask import Flask, request, jsonify, render_template, Blueprint
from database.db import db
from models.pergunta import Pergunta
from models.categoria import Categoria
from models.Etiqueta import Etiqueta

home_route = Blueprint('home', __name__, template_folder='../../front-end/templates')

@home_route.route('/')
def home():
    categoria_id = request.args.get('categoria')
    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()
    
    if categoria_id:
        perguntas = Pergunta.query.filter_by(codCategoria=categoria_id).order_by(Pergunta.data_criacao.desc()).all()

    else:
        perguntas = Pergunta.query.order_by(Pergunta.data_criacao.desc()).all()

    return render_template('home.html', perguntas=perguntas, categorias=categorias, etiquetas=etiquetas)
