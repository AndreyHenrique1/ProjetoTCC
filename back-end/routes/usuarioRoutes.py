from io import BytesIO
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from database.db import db
from models.usuario import Usuario
from models.pergunta import Pergunta
from models.blog import Blog
from models.comentariosPerguntas import comentariosPerguntas
import cloudinary.uploader
import random
import base64
from sqlalchemy import desc

usuario_route = Blueprint('usuario_route', __name__)

# Rota para exibir o perfil do usuário
@usuario_route.route('/perfil')
@login_required
def perfil():
    perguntas = Pergunta.query.filter_by(codUsuario=current_user.codigo).all()
    blogs = Blog.query.filter_by(codUsuario=current_user.codigo).all()
    respostas = comentariosPerguntas.query.filter_by(codUsuario=current_user.codigo).all()

    return render_template('perfil.html', perguntas=perguntas, blogs=blogs, respostas=respostas)

# Rota para atualizar as novas atualizações de informações do usuário 
@usuario_route.route('/editar_perfil', methods=['POST'])
@login_required
def editar_perfil():
    novo_nome = request.form.get('nomeUsuario')
    if novo_nome:
        current_user.nomeUsuario = novo_nome
        db.session.commit()
        flash('Nome de usuário atualizado com sucesso!')

    if 'imagem' not in request.files:
        flash('Nenhuma imagem selecionada.')
        return redirect(url_for('usuario_route.perfil'))

    imagem = request.files['imagem']
    if imagem.filename == '':
        flash('Arquivo inválido.')
        return redirect(url_for('usuario_route.perfil'))

    # Faz o upload da imagem para o Cloudinary e obtém a URL segura
    upload_result = cloudinary.uploader.upload(imagem, folder="fotos_perfil")
    url_imagem = upload_result.get('secure_url')  

    # Atualiza o campo `foto_perfil` no banco de dados
    if url_imagem:
        current_user.foto_perfil = url_imagem
        db.session.commit()

        print(f"Imagem salva com sucesso: {current_user.foto_perfil}")
    else:
        flash('Erro ao obter a URL da imagem.')

    return redirect(url_for('usuario_route.perfil'))

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
