from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import db
from models.pergunta import Pergunta
from models.comentariosPerguntas import comentariosPerguntas 
from models.categoria import Categoria
from models.curtidasComentarios import CurtidasComentarios  # Importando o modelo de curtidas
from models.usuario import Usuario
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

pergunta_route = Blueprint('pergunta_route', __name__)

@pergunta_route.route('/perguntar', methods=['GET', 'POST'])
@login_required
def perguntar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        codCategoria = request.form['categorias']
        codUsuario = current_user.codigo

        nova_pergunta = Pergunta(titulo=titulo, descricao=descricao, codCategoria=codCategoria, codUsuario=codUsuario)
        db.session.add(nova_pergunta)
        db.session.commit()

        return redirect(url_for('home.home'))

    categorias = Categoria.query.all()
    return render_template('perguntar.html', categorias=categorias)

# Rota para editar perguntas
@pergunta_route.route('/pergunta/<int:pergunta_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    
    if pergunta.codUsuario != current_user.codigo:
        flash("Você não tem permissão para editar essa pergunta.")
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        pergunta.titulo = request.form['titulo']
        pergunta.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=pergunta_id))

    return render_template('editar_pergunta.html', pergunta=pergunta)

# Rota para excluir perguntas
@pergunta_route.route('/pergunta/<int:pergunta_id>/excluir', methods=['POST'])
@login_required
def excluir_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    
    if pergunta.codUsuario != current_user.codigo:
        flash("Você não tem permissão para excluir essa pergunta.")
        return redirect(url_for('home.home'))

    # Excluir todos os comentários relacionados à pergunta
    comentariosPerguntas.query.filter_by(codPergunta=pergunta.codigo).delete()

    db.session.delete(pergunta)
    db.session.commit()
    return redirect(url_for('home.home'))

# Detalhes e comentários da pergunta
@pergunta_route.route('/pergunta/<int:pergunta_id>', methods=['GET', 'POST'])
def pergunta_detalhe(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)

    if request.method == 'POST':
        conteudo_comentario = request.form.get('conteudo_comentario')

        if conteudo_comentario and current_user.is_authenticated:
            novo_comentario = comentariosPerguntas(
                comentario=conteudo_comentario, codPergunta=pergunta_id, codUsuario=current_user.codigo
            )
            db.session.add(novo_comentario)
            db.session.commit()

            return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=pergunta_id))

    comentarios = comentariosPerguntas.query.filter_by(codPergunta=pergunta_id).all()

    return render_template('pergunta_detalhe.html', pergunta=pergunta, comentarios=comentarios)

# Rota para excluir comentário
@pergunta_route.route('/comentario/<int:comentario_id>/excluir', methods=['POST'])
@login_required
def excluir_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)

    if comentario.codUsuario != current_user.codigo:
        flash("Você não tem permissão para excluir esse comentário.")
        return redirect(url_for('home.home'))

    try:
        db.session.delete(comentario)
        db.session.commit()
        flash("Comentário excluído com sucesso.")
    except IntegrityError:
        db.session.rollback()
        flash("Ocorreu um erro ao excluir o comentário.")
    
    return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=comentario.codPergunta))

# Rota para curtir um comentário
@pergunta_route.route('/comentario/<int:comentario_id>/curtir', methods=['POST'])
@login_required
def curtir_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)

    # Verifica se o usuário já curtiu o comentário
    curtida_existente = CurtidasComentarios.query.filter_by(codUsuario=current_user.codigo, codComentario=comentario_id).first()
    if curtida_existente:
        flash('Você já curtiu este comentário.')
        return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=comentario.codPergunta))

    # Adiciona uma nova curtida
    nova_curtida = CurtidasComentarios(codComentario=comentario_id, codUsuario=current_user.codigo)
    db.session.add(nova_curtida)

    # Incrementa a quantidade de curtidas no comentário
    comentario.quantidadeCurtidas += 1
    db.session.commit()

    # Incrementa pontos ao dono do comentário
    dono_comentario = Usuario.query.get(comentario.codUsuario)
    dono_comentario.quantidadePontos += 1  # Adiciona 1 ponto
    db.session.commit()

    flash('Comentário curtido com sucesso!')
    return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=comentario.codPergunta))
