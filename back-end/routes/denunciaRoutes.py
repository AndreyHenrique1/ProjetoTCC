from flask import Blueprint, render_template, request, redirect, url_for
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

            # Garante que a quantidade de pontos não seja menor que zero
            if usuario_comentario.quantidadePontos < 0:
                usuario_comentario.quantidadePontos = 0

            db.session.commit()

        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta, sucesso="comentario_denunciado"))

    return render_template('detalhes_pergunta.html', comentario=comentario)

# Rota para moderadores concorda ou discorda de uma denuncia
@denuncia_route.route('/resolver/denuncia/<int:denuncia_id>', methods=['POST'])
@login_required
def resolver_denuncia(denuncia_id):
    # Buscar a denúncia usando o denuncia_id
    denuncia = Denuncia.query.get_or_404(denuncia_id)

    # Verificar se o usuário atual é moderador (300 pontos ou mais)
    if current_user.quantidadePontos < 300:
        # Verificar se a denúncia é de uma pergunta
        if denuncia.codPergunta:
            return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=denuncia.codPergunta))
        # Ou de um blog
        else:
            return redirect(url_for('blog_route.detalhes_blog', blog_id=denuncia.codBlog))

    # Identificar a ação do formulário
    acao = request.form.get('acao')
    if acao is None:
        # Se não houver ação, redireciona para a pergunta ou blog
        if denuncia.codPergunta:
            return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=denuncia.codPergunta))
        else:
            return redirect(url_for('blog_route.detalhes_blog', blog_id=denuncia.codBlog))

    if acao == "concordar":
        # Marcar a denúncia como verificada
        denuncia.verificada = True
        db.session.commit()

        # Redirecionar com mensagem de sucesso para pergunta ou blog
        if denuncia.codPergunta:
            return redirect(url_for(
                'pergunta_route.detalhes_pergunta',
                pergunta_id=denuncia.codPergunta,
                sucesso="denuncia_verificada",
                verificada="Denúncia verificada por moderador"
            ))
        else:
            return redirect(url_for(
                'blog_route.detalhes_blog',
                blog_id=denuncia.codBlog,
                sucesso="denuncia_verificada",
                verificada="Denúncia verificada por moderador"
            ))

    elif acao == "discordar":
        # Se a denúncia for de comentário
        if denuncia.codComentario:
            comentario = comentariosPerguntas.query.get_or_404(denuncia.codComentario)
            usuario_comentario = Usuario.query.get(comentario.codUsuario)
            db.session.delete(denuncia)

            # Restaurar pontos ao autor do comentário, se existir
            if usuario_comentario:
                usuario_comentario.quantidadePontos += 5
                db.session.commit()

            # Redirecionar com mensagem de denúncia removida para a pergunta
            return redirect(url_for(
                'pergunta_route.detalhes_pergunta',
                pergunta_id=denuncia.codPergunta,
                sucesso="denuncia_removida"
            ))
        # Se a denúncia for de blog
        elif denuncia.codBlog:
            db.session.delete(denuncia)
            db.session.commit()

            # Redirecionar com mensagem de denúncia removida para o blog
            return redirect(url_for(
                'blog_route.detalhes_blog',
                blog_id=denuncia.codBlog,
                sucesso="denuncia_removida"
            ))

    # Redirecionamento padrão caso nenhuma ação seja válida
    if denuncia.codPergunta:
        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=denuncia.codPergunta))
    else:
        return redirect(url_for('blog_route.detalhes_blog', blog_id=denuncia.codBlog))


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
        if blog.usuario_relacionado:  
            blog.usuario_relacionado.quantidadePontos -= 5

            # Garante que a quantidade de pontos não seja menor que zero
            if blog.usuario_relacionado.quantidadePontos < 0:
                blog.usuario_relacionado.quantidadePontos = 0

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
