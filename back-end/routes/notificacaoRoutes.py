# notificacaoRoutes.py
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.notificacao import Notificacao
from database.db import db

notificacao_route = Blueprint('notificacao_route', __name__)

# Exibir as notificações do usuário
@notificacao_route.route('/notificacoes')
@login_required
def listar_notificacoes():
    notificacoes = Notificacao.query.filter_by(codUsuario=current_user.codigo).order_by(Notificacao.data_criacao.desc()).all()
    return render_template('notificacoes.html', notificacoes=notificacoes)

# Marcar notificação como lida
@notificacao_route.route('/notificacao/<int:notificacao_id>/deletar', methods=['POST'])
@login_required
def deletar_notificacao(notificacao_id):
    notificacao = Notificacao.query.get_or_404(notificacao_id)

    if notificacao.codUsuario != current_user.codigo:
        flash("Você não tem permissão para acessar essa notificação.")
        return redirect(url_for('notificacao_route.listar_notificacoes'))

    db.session.delete(notificacao)  # Remove a notificação do banco de dados
    db.session.commit()

    flash("Notificação excluída com sucesso.")  # Confirmação
    return redirect(url_for('notificacao_route.listar_notificacoes'))  # Redireciona de volta



