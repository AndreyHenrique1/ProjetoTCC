from flask import Blueprint, render_template, request, redirect, url_for
from database.db import db
from models.pergunta import Pergunta
from models.comentariosPerguntas import comentariosPerguntas 
from models.categoria import Categoria
from flask_login import current_user

pergunta_route = Blueprint('pergunta_route', __name__)

@pergunta_route.route('/perguntar', methods=['GET', 'POST'])
def perguntar():
    # Se o método for POST
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

@pergunta_route.route('/pergunta/<int:pergunta_id>', methods=['GET', 'POST'])
def pergunta_detalhe(pergunta_id):
    # Tenta obter a pergunta com o ID fornecido. Se não for encontrada, retorna um erro 404.
    pergunta = Pergunta.query.get_or_404(pergunta_id)

    # Se o método for POST, processa a resposta
    if request.method == 'POST':
        conteudo_resposta = request.form.get('conteudo_resposta')
        
        if conteudo_resposta:
            # Cria uma nova resposta e salva no banco de dados
            nova_resposta = comentariosPerguntas(conteudo=conteudo_resposta, pergunta_id=pergunta_id, usuario_id=current_user.codigo)
            db.session.add(nova_resposta)
            db.session.commit()

            return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=pergunta_id))

    # Consultar todas as respostas associadas à pergunta
    respostas = comentariosPerguntas.query.filter_by(pergunta_id=pergunta_id).all()

    # Renderiza o template 'pergunta_detalhe.html' e passa a pergunta e as respostas encontradas como contexto
    return render_template('pergunta_detalhe.html', pergunta=pergunta, respostas=respostas)
