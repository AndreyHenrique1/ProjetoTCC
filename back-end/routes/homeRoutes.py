from flask import Flask, request, jsonify, render_template, Blueprint
from database.db import db
from models.pergunta import Pergunta
from models.categoria import Categoria

home_route = Blueprint('home', __name__, template_folder='../../front-end/templates')

@home_route.route('/')
def home():
    # Obtém as categorias e perguntas do banco e envia para a home
    categorias = Categoria.query.all()
    perguntas = Pergunta.query.order_by(Pergunta.data_criacao.desc()).all()
    return render_template('home.html', perguntas=perguntas, categorias=categorias)

