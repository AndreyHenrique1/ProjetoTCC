from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import db
from models.blog import Blog
from models.comentariosBlog import comentariosBlog
from models.categoria import Categoria
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
import cloudinary.uploader

blog_route = Blueprint('blog_route', __name__)

# Rota para listar todos os blogs
@blog_route.route('/blogs')
def listar_blogs():
    categoria_id = request.args.get('categoria')
    categorias = Categoria.query.all()
    
    if categoria_id:
        blogs = Blog.query.filter_by(codCategoria=categoria_id).order_by(Blog.data_criacao.desc()).all()
    else:
        blogs = Blog.query.order_by(Blog.data_criacao.desc()).all()
    return render_template('listar_blogs.html', blogs=blogs, categorias=categorias)

# Rota para exibir os detalhes de um blog específico
@blog_route.route('/blogs/<int:blog_id>')
def detalhes_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return render_template('detalhes_blog.html', blog=blog)

# Rota para criar um novo blog, somente para usuários logados
@blog_route.route('/blogs/novo', methods=['GET', 'POST'])
@login_required
def criar_blog():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        codCategoria = request.form['categorias']
        codUsuario = current_user.codigo

        # Verifique se o arquivo está presente na requisição
        if 'imagem' not in request.files:
            flash('Nenhuma imagem selecionada.')
            return redirect(request.url)

        imagem = request.files['imagem']

        # Valide o arquivo enviado
        if imagem.filename == '':
            flash('Arquivo inválido.')
            return redirect(request.url)

        
        # Faça o upload da imagem para o Cloudinary
        upload_result = cloudinary.uploader.upload(imagem, folder="fotos_perfil")
        url_imagem = upload_result.get('secure_url')

        # Atualize a imagem de capa do blog do usuário
        if url_imagem:
            current_user.fotoCapa_blog = url_imagem
            db.session.commit()

        else:
            flash('Erro ao obter a URL da imagem.')

        # Crie uma nova postagem de blog e salve no banco de dados
        novo_blog = Blog(titulo=titulo, descricao=descricao, codUsuario=codUsuario, codCategoria=codCategoria)
        db.session.add(novo_blog)
        db.session.commit()

        return redirect(url_for('blog_route.listar_blogs'))

    categorias = Categoria.query.all()
    return render_template('criar_blog.html', categorias=categorias)

@blog_route.route('/blogs/<int:blog_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if blog.codUsuario != current_user.codigo:
        flash("Você não tem permissão para editar esse blog.")
        return redirect(url_for('blog_route.listar_blogs'))

    if request.method == 'POST':
        blog.titulo = request.form['titulo']
        blog.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id))

    return render_template('editar_blog.html', blog=blog)

@blog_route.route('/blogs/<int:blog_id>/excluir', methods=['POST'])
@login_required
def excluir_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if blog.codUsuario != current_user.codigo:
        flash("Você não tem permissão para excluir esse blog.")
        return redirect(url_for('blog_route.listar_blogs'))

    comentariosBlog.query.filter_by(codBlog=blog.codigo).delete()

    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('blog_route.listar_blogs'))

# Detalhes e comentários da blog
@blog_route.route('/blog/<int:blog_id>', methods=['GET', 'POST'])
def blog_detalhe(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if request.method == 'POST':
        conteudo_comentario = request.form.get('conteudo_comentario')

        if conteudo_comentario and current_user.is_authenticated:
            novo_comentario = comentariosBlog(
                comentario=conteudo_comentario, codBlog=blog_id, codUsuario=current_user.codigo
            )
            db.session.add(novo_comentario)
            db.session.commit()

            return redirect(url_for('blog_route.blog_detalhe', blog_id=blog_id))

    comentarios = comentariosBlog.query.filter_by(codBlog=blog_id).all()

    return render_template('detalhes_blog.html', blog=blog, comentarios=comentarios) 

# Rota para excluir comentário
@blog_route.route('/comentario/<int:comentario_id>/excluir', methods=['POST'])
@login_required
def excluir_comentario(comentario_id):
    comentario = comentariosBlog.query.get_or_404(comentario_id)

    # Resto da lógica...

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
    
    return redirect(url_for('blog_route.blog_detalhe', blog_id=comentario.codBlog))