from flask import Blueprint, render_template, request, redirect, url_for
from database.db import db
from models.blog import Blog
from models.categoria import Categoria
from flask_login import current_user, login_required

blog_route = Blueprint('blog_route', __name__)

# Rota para listar todos os blogs
@blog_route.route('/blogs')
def listar_blogs():
    blogs = Blog.query.order_by(Blog.data_criacao.desc()).all()
    return render_template('listar_blogs.html', blogs=blogs)

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
        codCategoria = request.form['categoria']
        codUsuario = current_user.codigo

        # Cria uma nova postagem de blog e salva no banco de dados
        novo_blog = Blog(titulo=titulo, descricao=descricao, codUsuario=codUsuario, codCategoria=codCategoria)
        db.session.add(novo_blog)
        db.session.commit()

        return redirect(url_for('blog_route.listar_blogs'))

    categorias = Categoria.query.all()
    return render_template('criar_blog.html', categorias=categorias)
