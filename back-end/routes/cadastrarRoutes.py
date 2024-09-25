from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from models.usuario import Usuario
from database.db import db
import cloudinary.uploader

cadastrar_route = Blueprint('cadastrar_route', __name__)

@cadastrar_route.route('/cadastrar', methods=['GET', 'POST'])
@cadastrar_route.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        email = request.form['email']
        nomeCompleto = request.form.get('nomeCompleto')
        nomeUsuario = request.form['nomeUsuario']
        senha = request.form['senha']

        # Verificação de usuário existente
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Esse e-mail já está cadastrado.', 'danger')
            return redirect(url_for('cadastrar_route.cadastrar'))
        
        usuario_existente_nome = Usuario.query.filter_by(nomeUsuario=nomeUsuario).first()
        if usuario_existente_nome:
            flash('Esse nome de usuário já está sendo usado. Escolha outro.', 'danger')
            return redirect(url_for('cadastrar_route.cadastrar'))

        # Upload de imagem de perfil
        if 'imagem' not in request.files or request.files['imagem'].filename == '':
            flash('Selecione uma imagem para o perfil.', 'danger')
            return redirect(url_for('cadastrar_route.cadastrar'))

        imagem = request.files['imagem']

        try:
            upload_result = cloudinary.uploader.upload(imagem, folder="fotos_perfil")
            url_imagem = upload_result['secure_url']
        except Exception as e:
            flash(f"Erro ao fazer upload da imagem: {str(e)}", 'danger')
            return redirect(url_for('cadastrar_route.cadastrar'))

        # Adiciona o novo usuário ao banco de dados
        usuario = Usuario(email=email, nomeCompleto=nomeCompleto, nomeUsuario=nomeUsuario, senha=senha, foto_perfil=url_imagem)
        db.session.add(usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login_route.login'))

    return render_template("cadastrar.html")

@cadastrar_route.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    nomeUsuario = request.json.get('nomeUsuario')
    usuario_existente = Usuario.query.filter_by(nomeUsuario=nomeUsuario).first()
    if usuario_existente:
        return {'existe': True}
    return {'existe': False}
