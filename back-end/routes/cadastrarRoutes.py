from flask import Flask, render_template, Blueprint, request, redirect, url_for
from models.usuario import Usuario
from database.db import db

cadastrar_route = Blueprint('cadastrar_route', __name__)

@cadastrar_route.route('/cadastrar', methods=['GET', 'POST'])
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


