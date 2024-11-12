from io import BytesIO
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from database.db import db
from models.usuario import Usuario
from models.pergunta import Pergunta
from models.blog import Blog
from models.perguntasEtiquetas import PerguntasEtiquetas
from models.etiqueta import Etiqueta
from models.comentariosPerguntas import comentariosPerguntas
from models.denuncia import Denuncia
import cloudinary.uploader
from collections import Counter
from sqlalchemy import desc

usuario_route = Blueprint('usuario_route', __name__)

# Função para obter o ranking e a medalha correspondente
def obter_ranking_e_medalha(user_id):
    usuarios = Usuario.query.order_by(Usuario.quantidadePontos.desc()).all()
    for posicao, usuario in enumerate(usuarios, start=1):
        if usuario.codigo == user_id:
            # Define a cor da medalha com base na classificação
            if posicao == 1:
                medalha = {"cor": "gold", "numero": posicao}
            elif posicao == 2:
                medalha = {"cor": "silver", "numero": posicao}
            elif posicao == 3:
                medalha = {"cor": "bronze", "numero": posicao}
            else:
                medalha = {"cor": "black", "numero": posicao}
            return posicao, medalha
    return None, None  

# Rota para exibir o perfil do usuário
@usuario_route.route('/perfil')
@login_required
def perfil():
    sobre_usuario = current_user.sobre
    tags_mais_usadas = obter_etiquetas_mais_usadas(current_user.codigo)

    perguntas = Pergunta.query.filter_by(codUsuario=current_user.codigo).all()
    blogs = Blog.query.filter_by(codUsuario=current_user.codigo).all()
    respostas = comentariosPerguntas.query.filter_by(codUsuario=current_user.codigo).all()

    # Contagem das atividades do usuário
    perguntas_count = Pergunta.query.filter_by(codUsuario=current_user.codigo).count()
    blogs_count = Blog.query.filter_by(codUsuario=current_user.codigo).count()
    respostas_count = comentariosPerguntas.query.filter_by(codUsuario=current_user.codigo).count()
    denuncias_count = Denuncia.query.filter_by(codUsuario=current_user.codigo).count()

    # Obtém o ranking e a medalha do usuário atual
    ranking, medalha = obter_ranking_e_medalha(current_user.codigo)

    return render_template(
        'perfil.html',
        perguntas=perguntas,
        blogs=blogs,
        respostas=respostas,
        perguntas_count=perguntas_count,
        blogs_count=blogs_count,
        respostas_count=respostas_count,
        denuncias_count=denuncias_count,
        sobre=sobre_usuario,
        ranking=ranking,
        medalha=medalha,
        etiquetas_mais_usadas=tags_mais_usadas,
        usuario=current_user  
    )

# Rota para atualizar as novas atualizações de informações do usuário 
@usuario_route.route('/editar_perfil', methods=['POST'])
@login_required
def editar_perfil():
    novo_nome = request.form.get('nomeUsuario')
    sobre = request.form.get('sobre')

    # Atualiza o campo 'sobre' no banco de dados, se fornecido
    if sobre:
        current_user.sobre = sobre

    # Atualiza o nome de usuário, se fornecido
    if novo_nome:
        current_user.nomeUsuario = novo_nome

    # Verifica se uma imagem foi selecionada
    if 'imagem' in request.files and request.files['imagem'].filename != '':
        imagem = request.files['imagem']

        # Faz o upload da imagem para o Cloudinary e obtém a URL segura
        upload_result = cloudinary.uploader.upload(imagem, folder="fotos_perfil")
        url_imagem = upload_result.get('secure_url')

        # Atualiza o campo `foto_perfil` no banco de dados, se uma nova imagem foi enviada
        if url_imagem:
            current_user.foto_perfil = url_imagem

    db.session.commit()

    return redirect(url_for('usuario_route.perfil', sucesso="usuario_editado"))

# Rota da lista de usuários
@usuario_route.route('/usuarios')
def listar_usuarios():
    search_query = request.args.get('search')  # Obtém o nome do usuário a partir da query string
    if search_query:
        # Filtra os usuários que contêm a string da pesquisa no nome
        usuarios = Usuario.query.filter(Usuario.nomeUsuario.ilike(f'%{search_query}%')).order_by(desc(Usuario.quantidadePontos)).all()
    else:
        # Se não houver pesquisa, obtém todos os usuários ordenados por quantidade de pontos
        usuarios = Usuario.query.order_by(desc(Usuario.quantidadePontos)).all()

    return render_template('listar_usuarios.html', usuarios=usuarios)

# Função para obter as etiquetas mais usadas
def obter_etiquetas_mais_usadas(user_id):
    # Obter todas as perguntas do usuário
    perguntas = Pergunta.query.filter_by(codUsuario=user_id).all()
    
    # Coletar todas as etiquetas associadas a essas perguntas
    todas_etiquetas = []
    for pergunta in perguntas:
        # Obter os códigos de etiqueta associadas à pergunta
        etiquetas = PerguntasEtiquetas.query.filter_by(codPergunta=pergunta.codigo).all()
        todas_etiquetas.extend([tag.codEtiqueta for tag in etiquetas])
    
    # Contar as etiquetas
    contagem_etiquetas = Counter(todas_etiquetas)

    # Criar uma lista com as 5 etiquetas mais comuns
    etiquetas_mais_usadas = []
    for codEtiqueta, count in contagem_etiquetas.most_common(5):
        etiqueta = Etiqueta.query.get(codEtiqueta)  # Obter a etiqueta pelo código
        if etiqueta:
            etiquetas_mais_usadas.append((etiqueta.nome, count))  # Adicionar o nome da etiqueta e a contagem
    
    return etiquetas_mais_usadas

@usuario_route.route('/perfil/<int:user_id>')
def perfil_outro_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for('home.homePergunta'))
    
    # Obtendo informações do usuário que está sendo visualizado
    tags_mais_usadas = obter_etiquetas_mais_usadas(usuario.codigo)
    perguntas = Pergunta.query.filter_by(codUsuario=usuario.codigo).all()
    blogs = Blog.query.filter_by(codUsuario=usuario.codigo).all()
    respostas = comentariosPerguntas.query.filter_by(codUsuario=usuario.codigo).all()

    perguntas_count = Pergunta.query.filter_by(codUsuario=usuario.codigo).count()
    blogs_count = Blog.query.filter_by(codUsuario=usuario.codigo).count()
    respostas_count = comentariosPerguntas.query.filter_by(codUsuario=usuario.codigo).count()

    ranking, medalha = obter_ranking_e_medalha(usuario.codigo)

    return render_template(
        'perfil.html',
        usuario=usuario,
        perguntas=perguntas,
        blogs=blogs,
        respostas=respostas,
        perguntas_count=perguntas_count,
        blogs_count=blogs_count,
        respostas_count=respostas_count,
        ranking=ranking,
        medalha=medalha,
        etiquetas_mais_usadas=tags_mais_usadas
    )


