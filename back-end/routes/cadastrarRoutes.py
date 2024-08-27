from flask import Flask, render_template, Blueprint, request, redirect, url_for
from models.usuario import Usuario
from database.db import db
from flask_login import login_user, logout_user

cadastrar_route = Blueprint('cadastrar', __name__, template_folder='../../front-end/templates', url_prefix='/Cadastrar')

@cadastrar_route.route('/', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        email = request.form['email']
        nomeCompleto = request.form['nomeCompleto']
        nomeUsuario = request.form['nomeUsuario']
        senha = request.form['senha']

        usuario = Usuario(email, nomeCompleto, nomeUsuario, senha)
        db.session.add(usuario)
        db.session.commit()  

    return render_template("cadastrar.html")


