from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database.db import db
from models.blog import Blog
from models.comentariosBlog import comentariosBlog
from models.categoria import Categoria
from models.etiqueta import Etiqueta
from models.blogsEtiquetas import BlogsEtiquetas
from flask_login import current_user, login_required
import cloudinary.uploader
from sqlalchemy import func
from models.likes_deslikes import Likes_deslikes
from models.usuario import Usuario
from models.notificacao import enviar_notificacao

blog_route = Blueprint('blog_route', __name__)

@blog_route.route('/blogs')
def listar_blogs():
    categorias_selecionadas = request.args.getlist('categorias')
    etiquetas_selecionadas = request.args.get('etiquetas')
    ordenar_por = request.args.get('ordenar', 'recentes')  
    page = request.args.get('page', 1, type=int)  

    blogs = Blog.query

    # Filtra por categorias
    if categorias_selecionadas:
        blogs = blogs.filter(Blog.codCategoria.in_(categorias_selecionadas))

    # Filtra por etiquetas
    if etiquetas_selecionadas:
        etiquetas_selecionadas = [etiqueta.lstrip('#').strip() for etiqueta in etiquetas_selecionadas.split(',')]
        blogs = blogs.join(BlogsEtiquetas).join(Etiqueta)\
                     .filter(Etiqueta.nome.in_(etiquetas_selecionadas))\
                     .group_by(Blog.codigo)\
                     .having(func.count(Etiqueta.codigo) == len(etiquetas_selecionadas))

    # Ordena os blogs
    if ordenar_por == 'recentes':
        blogs = blogs.order_by(Blog.data_criacao.desc())
    elif ordenar_por == 'antigas':
        blogs = blogs.order_by(Blog.data_criacao.asc())

    # Pagina os blogs
    per_page = 16  
    blogs_paginados = blogs.paginate(page=page, per_page=per_page, error_out=False)

    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()

    return render_template('listar_blogs.html', blogs=blogs_paginados.items, 
                           pagination=blogs_paginados, categorias=categorias, etiquetas=etiquetas)

# Rota para criar um novo blog, somente para usuários logados
@blog_route.route('/blogs/novo', methods=['GET', 'POST'])
@login_required
def criar_blog():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        codCategoria = request.form['categorias']
        etiquetas_input = request.form['Etiqueta']
        codUsuario = current_user.codigo

        # Separando as etiquetas por # e removendo espaços 
        etiquetas_lista = [et.strip().lstrip('#') for et in etiquetas_input.split('#') if et.strip()]  

        # Verifique se o arquivo está presente na requisição
        if 'imagem' not in request.files:
            return redirect(request.url)

        imagem = request.files['imagem']

        # Valide o arquivo enviado
        if imagem.filename == '':
            return redirect(request.url)

        # Faça o upload da imagem para o Cloudinary
        upload_result = cloudinary.uploader.upload(imagem, folder="fotos_capa_blog")
        url_imagem = upload_result.get('secure_url')

        # Crie uma nova postagem de blog com a imagem de capa
        novo_blog = Blog(
            titulo=titulo,
            descricao=descricao,
            codUsuario=codUsuario,
            codCategoria=codCategoria,
            fotoCapa_blog=url_imagem  
        )
        db.session.add(novo_blog)
        db.session.commit()

        # Pega cada etiqueta separadamente
        for nome_etiqueta in etiquetas_lista:
            etiqueta_objeto = Etiqueta.query.filter_by(nome=nome_etiqueta).first()

            # Verifica se a etiqueta já existe
            if etiqueta_objeto:
                # Caso exista a etiqueta aumenta +1 na popularidade
                etiqueta_objeto.popularidade += 1
            else:
                # Cria uma nova etiqueta
                etiqueta_objeto = Etiqueta(nome=nome_etiqueta, popularidade=1)
                db.session.add(etiqueta_objeto)
                db.session.commit() 

            # Associa a etiqueta ao blog
            nova_pergunta_etiqueta = BlogsEtiquetas(codBlog=novo_blog.codigo, codEtiqueta=etiqueta_objeto.codigo)
            db.session.add(nova_pergunta_etiqueta)

        # Commit final para associar etiquetas e blog
        db.session.commit()

        # Aumentar 3 pontos para o dono do blog
        usuario_blog = Usuario.query.get(novo_blog.codUsuario)  # Usuário que criou o blog
        if usuario_blog:
            usuario_blog.quantidadePontos += 3  # Adiciona 3 pontos
            db.session.commit()

        return redirect(url_for('blog_route.listar_blogs', sucesso="blog_enviado"))

    categorias = Categoria.query.all()
    etiquetas = Etiqueta.query.all()
    return render_template('criar_blog.html', categorias=categorias, etiquetas=etiquetas)

# Rota para exibir os detalhes de um blog específico
@blog_route.route('/blogs/<int:blog_id>')
def detalhes_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    comentarios = comentariosBlog.query.filter_by(codBlog=blog_id).all()  
    return render_template('detalhes_blog.html', blog=blog, comentarios=comentarios)

# Rota para editar um blog
@blog_route.route('/blogs/<int:blog_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Caso não seja o usuário que tenha criado o blog, ele não poderá editar
    if blog.codUsuario != current_user.codigo:
        return redirect(url_for('blog_route.listar_blogs'))

    if request.method == 'POST':
        blog.titulo = request.form['titulo']
        blog.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id, sucesso="blog_editado"))

    return render_template('editar_blog.html', blog=blog)

# Rota para excluir blog
@blog_route.route('/blogs/<int:blog_id>/excluir', methods=['POST'])
@login_required
def excluir_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Caso não seja o usuário que tenha criado o blog, ele não poderá excluir
    if blog.codUsuario != current_user.codigo:
        return redirect(url_for('blog_route.listar_blogs'))
    
    # Obter todas as etiquetas associadas ao blog
    etiquetas_associadas = BlogsEtiquetas.query.filter_by(codBlog=blog.codigo).all()

    # Excluir todas as associações que possuem na tabela BlogsEtiquetas
    for associacao in etiquetas_associadas:
        # Verifica se a etiqueta ainda está associada a outros blogs
        etiqueta = Etiqueta.query.get(associacao.codEtiqueta)
        
        if etiqueta:
            # Diminui a popularidade
            etiqueta.popularidade -= 1
            
            # Verifica se a popularidade é igual a 0, ou seja, não possui nenhum usuário com essa etiqueta
            if etiqueta.popularidade == 0:
                # Se não estiver associada a outros blogs, exclui a etiqueta
                if not BlogsEtiquetas.query.filter(BlogsEtiquetas.codEtiqueta == etiqueta.codigo).filter(BlogsEtiquetas.codBlog != blog.codigo).first():
                    db.session.delete(etiqueta)

        # Exclui a associação do BlogsEtiquetas
        db.session.delete(associacao)

    # Comita as mudanças para as associações e etiquetas processadas
    db.session.commit()

    # Excluir registros de `likes_deslikes` antes de excluir os comentários
    comentarios = comentariosBlog.query.filter_by(codBlog=blog.codigo).all()
    for comentario in comentarios:
        Likes_deslikes.query.filter_by(codComentarioBlog=comentario.codigo).delete()

    # Excluindo os comentários associados ao blog
    comentariosBlog.query.filter_by(codBlog=blog.codigo).delete()

    # Diminui 3 pontos do usuário que criou o blog
    usuario_blog = Usuario.query.get(blog.codUsuario)  
    if usuario_blog:
        usuario_blog.quantidadePontos -= 3  # Diminui 3 pontos
        db.session.commit()

    # Excluindo o blog
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('blog_route.listar_blogs', sucesso="blog_excluido"))

# Rota para comentários do blog
@blog_route.route('/blog/<int:blog_id>', methods=['GET', 'POST'])
def comentario_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if request.method == 'POST':
        conteudo_comentario = request.form.get('conteudo_comentario')

        if conteudo_comentario and current_user.is_authenticated:
            # Criação do novo comentário
            novo_comentario = comentariosBlog(
                comentario=conteudo_comentario, codBlog=blog_id, codUsuario=current_user.codigo
            )
            db.session.add(novo_comentario)
            db.session.commit()

            # Enviar notificação para o dono do blog
            if current_user.codigo != blog.codUsuario:
                mensagem = f"Novo comentário no seu blog: {blog.titulo}"
                link_blog = url_for('blog_route.detalhes_blog', blog_id=blog_id)

                # Passar codBlog para a notificação e codPergunta como None
                enviar_notificacao(
                    blog.codUsuario, 
                    mensagem, 
                    link_blog, 
                    codBlog=blog.codigo, 
                    codPergunta=None
                )

            return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id, sucesso="comentario_realizado"))

    comentarios = comentariosBlog.query.filter_by(codBlog=blog_id).all()

    return render_template('detalhes_blog.html', blog=blog, comentarios=comentarios)

# Rota para excluir comentário do blog
@blog_route.route('/comentario/<int:comentario_id>/excluir', methods=['POST', 'GET'])
@login_required
def excluir_comentario_blog(comentario_id):
    comentario = comentariosBlog.query.get_or_404(comentario_id)

    # Caso não seja o usuário que tenha criado o comentário, não poderá excluir
    if comentario.codUsuario != current_user.codigo:
        return redirect(url_for('home.homePergunta'))

    # Excluir registros relacionados na tabela 'likes_deslikes'
    db.session.query(Likes_deslikes).filter(Likes_deslikes.codComentarioBlog == comentario_id).delete()

    # Excluir comentário do blog
    db.session.delete(comentario)
    db.session.commit()

    return redirect(url_for('blog_route.detalhes_blog', blog_id=comentario.codBlog, sucesso="comentario_excluido"))

# Rota para aparecer as etiquetas no banco de dados ao clicar no input
@blog_route.route('/etiquetas_iniciais')
def etiquetas_iniciais():
    # Pega as cinco primeiras etiquetas do banco de dados
    etiquetas = Etiqueta.query.limit(5).all()
    etiquetas_json = [{'codigo': etiqueta.codigo, 'nome': etiqueta.nome} for etiqueta in etiquetas]
    return jsonify(etiquetas_json)

# Rota para pegar as etiquetas relacionadas de acordo com a pesquisa
@blog_route.route('/etiquetas_relacionadas')
def etiquetas_relacionadas():
    termo = request.args.get('termo', '')
    
    if termo:
        etiquetas = Etiqueta.query.filter(Etiqueta.nome.ilike(f'%{termo}%')).limit(5).all()
    else:
        etiquetas = []

    etiquetas_json = [{'codigo': etiqueta.codigo, 'nome': etiqueta.nome} for etiqueta in etiquetas]
    return jsonify(etiquetas_json)

# Rota para dar like em um comentario
@blog_route.route('/comentario_blog/<int:comentario_id>/curtir', methods=['POST'])
@login_required
def like_comentario_blog(comentario_id):
    comentario = comentariosBlog.query.get_or_404(comentario_id)

    # Verifica se o usuário já curtiu o comentário
    curtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codComentarioBlog=comentario_id, 
        tipo='like',
        origem='comentario_blog'  
    ).first()

    # Verifica se o usuário já deu deslike no comentário
    descurtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codComentarioBlog=comentario_id,  
        tipo='deslike',
        origem='comentario_blog' 
    ).first()

    if curtida_existente:
        # Se o usuário já deu like
        db.session.delete(curtida_existente)
        comentario.quantidadeCurtidas -= 1
        db.session.commit()

        # Decrementa pontos ao dono do comentário
        dono_comentario = Usuario.query.get(comentario.codUsuario)
        dono_comentario.quantidadePontos -= 1  
        db.session.commit()

    if descurtida_existente:
        # Se o usuário já deu deslike, retira o deslike e adiciona o like
        db.session.delete(descurtida_existente)  
        comentario.quantidadeCurtidas += 1 
        db.session.commit()

        # Incrementa pontos ao dono do comentário
        dono_comentario = Usuario.query.get(comentario.codUsuario)
        dono_comentario.quantidadePontos += 1 
        db.session.commit()

    # Adiciona uma nova curtida
    nova_curtida = Likes_deslikes(
        codComentarioBlog=comentario_id,  
        codUsuario=current_user.codigo,
        tipo='like',
        origem='comentario_blog'  
    )
    db.session.add(nova_curtida)

    # Incrementa a quantidade de curtidas no comentário
    comentario.quantidadeCurtidas += 1
    db.session.commit()

    # Incrementa pontos ao dono do comentário
    dono_comentario = Usuario.query.get(comentario.codUsuario)
    dono_comentario.quantidadePontos += 1 
    db.session.commit()

    return redirect(url_for('blog_route.detalhes_blog', blog_id=comentario.codBlog, sucesso="like_realizado"))

# Rota de deslike no comentario
@blog_route.route('/comentario_blog/<int:comentario_id>/descurtir', methods=['POST'])
@login_required
def deslike_comentario_blog(comentario_id):
    comentario = comentariosBlog.query.get_or_404(comentario_id)

    # Verifica se o usuário já deu deslike no comentário
    descurtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codComentarioBlog=comentario_id,  
        tipo='deslike',
        origem='comentario_blog'  
    ).first()

    # Verifica se o usuário já deu like no comentário
    curtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codComentarioBlog=comentario_id,  
        tipo='like',
        origem='comentario_blog'  
    ).first()

    if descurtida_existente:
        # Se o usuário já deu deslike, retira o deslike 
        db.session.delete(descurtida_existente)
        comentario.quantidadeCurtidas += 1  
        db.session.commit()

        # Incrementa pontos ao dono do comentário
        dono_comentario = Usuario.query.get(comentario.codUsuario)
        dono_comentario.quantidadePontos += 1 
        db.session.commit()

    if curtida_existente:
        # Se o usuário já deu like, retira o like e adiciona o deslike
        db.session.delete(curtida_existente)  
        comentario.quantidadeCurtidas -= 1  
        db.session.commit()

        # Decrementa pontos ao dono do comentário
        dono_comentario = Usuario.query.get(comentario.codUsuario)
        dono_comentario.quantidadePontos -= 1  
        db.session.commit()

    # Adiciona uma nova descurtida
    nova_descurtida = Likes_deslikes(
        codComentarioBlog=comentario_id,  
        codUsuario=current_user.codigo,
        tipo='deslike',
        origem='comentario_blog'  
    )
    db.session.add(nova_descurtida)

    # Decrementa a quantidade de curtidas no comentário
    comentario.quantidadeCurtidas -= 1
    db.session.commit()

    # Decrementa pontos ao dono do comentário 
    dono_comentario = Usuario.query.get(comentario.codUsuario)
    dono_comentario.quantidadePontos -= 1 
    db.session.commit()

    return redirect(url_for('blog_route.detalhes_blog', blog_id=comentario.codBlog, sucesso="deslike_realizado"))

# Função para curtir o blog
@blog_route.route('/like_blog/<int:blog_id>', methods=['POST'])
@login_required
def like_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Verifica se o usuário já curtiu o blog
    curtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codBlog=blog_id,
        tipo='like',
        origem='blog'
    ).first()

    # Verifica se o usuário já deu deslike no blog
    descurtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codBlog=blog_id,
        tipo='deslike',
        origem='blog'
    ).first()

    if curtida_existente:
        # Se o usuário já deu like, retira o like
        db.session.delete(curtida_existente)
        blog.quantidadeCurtidas -= 1
        db.session.commit()

        # Decrementa pontos ao autor do blog
        autor_blog = Usuario.query.get(blog.codUsuario)
        autor_blog.quantidadePontos -= 1  
        db.session.commit()

    if descurtida_existente:
        # Se o usuário já deu deslike, retira o deslike e adiciona o like
        db.session.delete(descurtida_existente)
        blog.quantidadeCurtidas += 1 
        db.session.commit()

        # Incrementa pontos ao autor do blog
        autor_blog = Usuario.query.get(blog.codUsuario)
        autor_blog.quantidadePontos += 1  
        db.session.commit()

    # Adiciona uma nova curtida
    nova_curtida = Likes_deslikes(
        codBlog=blog_id,
        codUsuario=current_user.codigo,
        tipo='like',
        origem='blog'
    )
    db.session.add(nova_curtida)

    # Incrementa a quantidade de curtidas no blog
    blog.quantidadeCurtidas += 1
    db.session.commit()

    # Incrementa pontos ao autor do blog
    autor_blog = Usuario.query.get(blog.codUsuario)
    autor_blog.quantidadePontos += 1
    db.session.commit()

    return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id, sucesso="like_realizado"))

# Função para descurtir o blog
@blog_route.route('/deslike_blog/<int:blog_id>', methods=['POST'])
@login_required
def deslike_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Verifica se o usuário já deu deslike no blog
    descurtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codBlog=blog_id,
        tipo='deslike',
        origem='blog'
    ).first()

    # Verifica se o usuário já deu like no blog
    curtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codBlog=blog_id,
        tipo='like',
        origem='blog'
    ).first()

    if descurtida_existente:
        # Se o usuário já deu deslike, retira o deslike 
        db.session.delete(descurtida_existente)
        blog.quantidadeCurtidas += 1  
        db.session.commit()

        # Incrementa pontos ao autor do blog
        autor_blog = Usuario.query.get(blog.codUsuario)
        autor_blog.quantidadePontos += 1  
        db.session.commit()

    if curtida_existente:
        # Se o usuário já deu like, retira o like e adiciona o deslike
        db.session.delete(curtida_existente)
        blog.quantidadeCurtidas -= 1 
        db.session.commit()

        # Decrementa pontos ao autor do blog 
        autor_blog = Usuario.query.get(blog.codUsuario)
        autor_blog.quantidadePontos -= 1  
        db.session.commit()

    # Adiciona uma nova descurtida
    nova_descurtida = Likes_deslikes(
        codBlog=blog_id,
        codUsuario=current_user.codigo,
        tipo='deslike',
        origem='blog'
    )
    db.session.add(nova_descurtida)

    # Decrementa a quantidade de curtidas no blog
    blog.quantidadeCurtidas -= 1
    db.session.commit()

    # Decrementa pontos ao autor do blog (se necessário)
    autor_blog = Usuario.query.get(blog.codUsuario)
    autor_blog.quantidadePontos -= 1 
    db.session.commit()

    return redirect(url_for('blog_route.detalhes_blog', blog_id=blog_id, sucesso="deslike_realizado"))

# Rota para a barra de pesquisa
@blog_route.route('/pesquisar_blog', methods=['POST'])
def blog_pesquisar():
    pesquisa = request.form.get('pesquisar')

    if pesquisa:
        # Busca os blogs cujo título ou descrição contenham o termo pesquisado no banco de dados 
        blogs_encontrados = Blog.query.filter(
            (Blog.titulo.ilike(f'%{pesquisa}%')) | 
            (Blog.descricao.ilike(f'%{pesquisa}%'))
        ).all()

        # Renderiza o template passando a lista de blogs encontrados
        return render_template('listar_blogs.html', blogs=blogs_encontrados, pesquisa=pesquisa)

    return redirect(url_for('blog_route.listar_blogs'))
