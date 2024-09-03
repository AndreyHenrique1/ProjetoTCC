from flask import Blueprint, render_template, request, redirect, url_for
from database.db import db
from models.pergunta import Pergunta

pergunta_route = Blueprint('pergunta_route', __name__)

@pergunta_route.route('/perguntar', methods=['GET', 'POST'])
def perguntar():
    print("Chegou aqui")
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']

        # Salvar nova pergunta no banco de dados
        nova_pergunta = Pergunta(titulo=titulo, descricao=descricao)
        db.session.add(nova_pergunta)
        db.session.commit()
        perguntas = Pergunta.query.all()
        print(perguntas)

        return redirect(url_for('home.home'))

    return render_template('perguntar.html')

@pergunta_route.route('/Teste')
def listar_perguntas():
    perguntas = Pergunta.query.order_by(Pergunta.data_criacao.desc()).all()
    return render_template('home.html', perguntas=perguntas)
