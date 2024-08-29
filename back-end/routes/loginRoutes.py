from flask import Flask, render_template, Blueprint, request, redirect, url_for
from models.usuario import Usuario
from flask_login import login_user, logout_user

login_route = Blueprint('login', __name__, template_folder='../../front-end/templates', url_prefix='/Login')

@login_route.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email, senha=senha).first()

        if not usuario or not usuario.verificar_senha(senha):
            print(f'Usuário encotrado: {usuario}')
            print(f'Senha encontrada: {senha}')
            return redirect(url_for('login.login'))       
        
        login_user(usuario)
        return redirect(url_for('home.home'))

    return render_template("login.html")

@login_route.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))