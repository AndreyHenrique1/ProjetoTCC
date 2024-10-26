from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.notificacao import Notificacao
from database.db import db

notificacao_route = Blueprint('notificacao_route', __name__)

# Exibir as notificações do usuário
@notificacao_route.route('/notificacoes')
@login_required
def listar_notificacoes():
    # Busca notificações do usuário autenticado, ordenadas por data de criação
    notificacoes = Notificacao.query.filter_by(codUsuario=current_user.codigo).order_by(Notificacao.data_criacao.desc()).all()
    return render_template('notificacoes.html', notificacoes=notificacoes)

# Rota para excluir notificacao
@notificacao_route.route('/notificacao/<int:notificacao_id>/deletar', methods=['POST'])
@login_required
def deletar_notificacao(notificacao_id):
    notificacao = Notificacao.query.get_or_404(notificacao_id)

    # Caso a notficação não esteja associada ao usuário
    if notificacao.codUsuario != current_user.codigo:
        return redirect(url_for('notificacao_route.listar_notificacoes'))

    # Remove a notificação
    db.session.delete(notificacao) 
    db.session.commit()

    return redirect(url_for('notificacao_route.listar_notificacoes'))  



