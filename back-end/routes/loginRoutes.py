from flask import Flask, render_template, Blueprint, request, redirect, url_for
from models.usuario import Usuario
from flask_login import login_user, logout_user

login_route = Blueprint('login_route', __name__)

@login_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Busca o usuário no banco de dados com base no email fornecido
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário existe e se a senha fornecida é correta
        if not usuario or not usuario.verificar_senha(senha):
            # Se o login falhar, renderiza a página de login com uma mensagem de erro
            return render_template("login.html", erro="E-mail ou senha incorretos.")

        # Caso o login seja bem-sucedido
        login_user(usuario)
        return redirect(url_for('home.home'))

    return render_template("login.html")

@login_route.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.home'))
