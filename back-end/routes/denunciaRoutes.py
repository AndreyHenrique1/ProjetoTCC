from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models.denuncia import Denuncia
from models.comentariosPerguntas import comentariosPerguntas
from models.usuario import Usuario
from models.blog import Blog
from database.db import db

denuncia_route = Blueprint('denuncia_route', __name__)

# Rota para enviar uma denúncia de comentário
@denuncia_route.route('/denunciar/comentario/<int:comentario_id>', methods=['GET', 'POST'])
@login_required
def denunciar_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)

    # Verifica se o comentário foi marcado como a melhor resposta
    if comentario.melhor_resposta:
        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta, sucesso="comentario_verificado_denunciado"))

    if request.method == 'POST':
        descricao_denuncia = request.form.get('descricao_denuncia')

        # Verifica se já existe uma denúncia para este comentário por este usuário
        existing_denuncia = Denuncia.query.filter_by(codComentario=comentario_id, codUsuario=current_user.codigo).first()
        if existing_denuncia:
            return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta, sucesso="comentario_ja_denunciado"))

        # Cria uma nova denúncia para o comentário
        nova_denuncia = Denuncia(
            codComentario=comentario_id,
            codPergunta=comentario.codPergunta,
            codUsuario=current_user.codigo,
            descricao=descricao_denuncia
        )
        db.session.add(nova_denuncia)

        # Decrementa 5 pontos do usuário que criou o comentário denunciado
        usuario_comentario = Usuario.query.get(comentario.codUsuario)
        if usuario_comentario:
            usuario_comentario.quantidadePontos -= 5  # Remove 5 pontos
            db.session.commit()

        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta, sucesso="comentario_denunciado"))

    return render_template('detalhes_pergunta.html', comentario=comentario)

# Rota para enviar uma denúncia de blog
@denuncia_route.route('/denunciar/blog/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def denunciar_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if request.method == 'POST':
        descricao_denuncia = request.form.get('descricao_denuncia')

        # Verifica se já existe uma denúncia para este blog por este usuário
        existing_denuncia = Denuncia.query.filter_by(codBlog=blog_id, codUsuario=current_user.codigo).first()
        if existing_denuncia:
            return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id, sucesso="blog_ja_denunciado"))

        # Cria uma nova denúncia para o blog
        nova_denuncia = Denuncia(codBlog=blog_id, codUsuario=current_user.codigo, descricao=descricao_denuncia)
        db.session.add(nova_denuncia)
        db.session.commit()

        # Reduz 5 pontos do usuário que criou o blog
        if blog.usuario_relacionado:  # Verifica se existe um usuário associado ao blog
            blog.usuario_relacionado.pontos -= 5
            db.session.commit()

        return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id, sucesso="blog_denunciado"))

    return render_template('detalhes_blog.html', blog=blog)

# Rota para ver as denúncias de um comentário específico
@denuncia_route.route('/denuncias/comentario/<int:comentario_id>')
@login_required
def ver_denuncias_comentario(comentario_id):
    denuncias = Denuncia.query.filter_by(codComentario=comentario_id).all()
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)
    return render_template('ver_denuncias.html', denuncias=denuncias, comentario=comentario)

# Rota para ver as denúncias de um blog específico
@denuncia_route.route('/denuncias/blog/<int:blog_id>')
@login_required
def ver_denuncias_blog(blog_id):
    denuncias = Denuncia.query.filter_by(codBlog=blog_id).all()
    blog = Blog.query.get_or_404(blog_id)
    return render_template('ver_denuncias_blog.html', denuncias=denuncias, blog=blog)
