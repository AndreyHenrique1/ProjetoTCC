from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.notificacao import Notificacao
from database.db import db

notificacao_route = Blueprint('notificacao_route', __name__)

# Exibir as notificações do usuário
@notificacao_route.route('/notificacoes')
@login_required
def listar_notificacoes():
    notificacoes = Notificacao.query.filter_by(codUsuario=current_user.codigo, lida=False).order_by(Notificacao.data_criacao.desc()).all()
    return render_template('notificacoes.html', notificacoes=notificacoes)

@notificacao_route.route('/notificacao/marcar_como_lida/<int:notificacao_id>', methods=['POST'])
def marcar_como_lida(notificacao_id):
    # Encontrando a notificação no banco de dados
    notificacao = Notificacao.query.get(notificacao_id)
    
    if notificacao:
        # Marcando como lida
        notificacao.lida = True
        db.session.commit()  

    return redirect(url_for('notificacao_route.listar_notificacoes'))






