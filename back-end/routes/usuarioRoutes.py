from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from models.usuario import Usuario
from database.db import db
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

usuario_route = Blueprint('usuario_route', __name__)

@usuario_route.route('/Usuário', methods=['GET', 'POST'])
@login_required
def usuario():
    return render_template('usuario.html')