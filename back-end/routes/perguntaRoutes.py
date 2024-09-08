from flask import Blueprint, render_template, request, redirect, url_for
from database.db import db
from models.pergunta import Pergunta
from models.categoria import Categoria 
from flask_login import current_user

pergunta_route = Blueprint('pergunta_route', __name__)

@pergunta_route.route('/perguntar', methods=['GET', 'POST'])
def perguntar():
    # Se o metedo for POST
    if request.method == 'POST':
        # Obtém os dados da pergunta
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        codCategoria = request.form['categorias'] 
        codUsuario = current_user.codigo

        # Salvar nova pergunta no banco de dados
        nova_pergunta = Pergunta(titulo=titulo, descricao=descricao, codCategoria=codCategoria, codUsuario=codUsuario)
        db.session.add(nova_pergunta)
        db.session.commit()

        return redirect(url_for('home.home'))
    
    # Consultar categorias e passar para o template
    categorias = Categoria.query.all()
    return render_template('perguntar.html', categorias=categorias)

@pergunta_route.route('/pergunta/<int:pergunta_id>')
def pergunta_detalhe(pergunta_id):
    # Tenta obter a pergunta com o ID fornecido. Se não for encontrada, retorna um erro 404.
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    # Renderiza o template 'pergunta_detalhe.html' e passa a pergunta encontrada como contexto.
    return render_template('pergunta_detalhe.html', pergunta=pergunta)

