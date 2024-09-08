from flask import Flask, request, jsonify, render_template, Blueprint
from database.db import db
from models.pergunta import Pergunta

home_route = Blueprint('home', __name__, template_folder='../../front-end/templates')

@home_route.route('/')
def home():
    # Pegar as perguntas do banco de dados e enviar ao home.html
    perguntas = Pergunta.query.order_by(Pergunta.data_criacao.desc()).all()
    return render_template('home.html', perguntas=perguntas)

