from flask import render_template, Blueprint, request, redirect, url_for
from models.usuario import Usuario
from flask_login import login_user, logout_user

login_route = Blueprint('login_route', __name__)

# Rota de login de usuários
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

        # Caso o login seja bem-sucedido, o usuário será logado
        login_user(usuario)
        return redirect(url_for('home.homePergunta'))

    return render_template("login.html")

# Rota para fazer o logout
@login_route.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.homePergunta'))
