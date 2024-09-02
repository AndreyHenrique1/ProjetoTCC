from flask import Flask, render_template, Blueprint, request, redirect, url_for
from models.usuario import Usuario
from flask_login import login_user, logout_user

login_route = Blueprint('login_route', __name__)

@login_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.verificar_senha(senha):
            return redirect(url_for('login_route.login'))       
        
        login_user(usuario)
        return redirect(url_for('home.home'))

    return render_template("login.html")

@login_route.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.home'))