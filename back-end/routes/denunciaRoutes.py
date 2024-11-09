from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models.denuncia import Denuncia
from models.comentariosPerguntas import comentariosPerguntas
from models.blog import Blog
from database.db import db

denuncia_route = Blueprint('denuncia_route', __name__)

# Rota para enviar uma denúncia de comentário
@denuncia_route.route('/denunciar/comentario/<int:comentario_id>', methods=['GET', 'POST'])
@login_required
def denunciar_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)
    
    if request.method == 'POST':
        descricao_denuncia = request.form.get('descricao_denuncia')
        
        # Verifica se já existe uma denúncia para este comentário por este usuário
        existing_denuncia = Denuncia.query.filter_by(codComentario=comentario_id, codUsuario=current_user.codigo).first()
        if existing_denuncia:
            flash('Você já denunciou este comentário.', 'warning')
            return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta))
        
        # Cria uma nova denúncia para o comentário
        nova_denuncia = Denuncia(codComentario=comentario_id, codPergunta=comentario.codPergunta, codUsuario=current_user.codigo, descricao=descricao_denuncia)
        db.session.add(nova_denuncia)
        db.session.commit()
        
        flash('Denúncia enviada com sucesso!', 'success')
        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta))
    
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
            return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id))
        
        # Cria uma nova denúncia para o blog
        nova_denuncia = Denuncia(codBlog=blog_id, codUsuario=current_user.codigo, descricao=descricao_denuncia)
        db.session.add(nova_denuncia)
        db.session.commit()
        
        return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id))
    
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
