from flask import Blueprint, render_template, request, redirect, url_for
from database.db import db
from models.pergunta import Pergunta
from models.comentariosPerguntas import comentariosPerguntas 
from models.categoria import Categoria
from flask_login import current_user

pergunta_route = Blueprint('pergunta_route', __name__)

@pergunta_route.route('/perguntar', methods=['GET', 'POST'])
def perguntar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        codCategoria = request.form['categorias'] 
        codUsuario = current_user.codigo

        # Salvar nova pergunta no banco de dados
        nova_pergunta = Pergunta(titulo=titulo, descricao=descricao, codCategoria=codCategoria, codUsuario=codUsuario)
        db.session.add(nova_pergunta)
        db.session.commit()

        return redirect(url_for('home.home'))
    
    categorias = Categoria.query.all()
    return render_template('perguntar.html', categorias=categorias)

@pergunta_route.route('/pergunta/<int:pergunta_id>', methods=['GET', 'POST'])
def pergunta_detalhe(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)

    if request.method == 'POST':
        conteudo_comentario = request.form.get('conteudo_comentario')
        
        if conteudo_comentario:
            # Cria um novo comentário e salva no banco de dados
            novo_comentario = comentariosPerguntas(comentario=conteudo_comentario, codPergunta=pergunta_id, codUsuario=current_user.codigo)
            db.session.add(novo_comentario)
            db.session.commit()

            return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=pergunta_id))

    # Consultar todos os comentários associados à pergunta
    comentarios = comentariosPerguntas.query.filter_by(codPergunta=pergunta_id).all()

    return render_template('pergunta_detalhe.html', pergunta=pergunta, comentarios=comentarios)
