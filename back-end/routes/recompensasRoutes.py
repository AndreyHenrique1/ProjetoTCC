from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from database.db import db
from models.recompensasResgatadas import RecompensasResgatadas
from models.recompensas import Recompensa
from models.usuario import Usuario
from sqlalchemy import desc

recompensas_route = Blueprint('recompensas', __name__, template_folder='../../front-end/templates')

# Rota de recompesa
@recompensas_route.route('/Recompensas')
def recompensas():
    recompensas = Recompensa.query.all()

    # Obter IDs das recompensas já resgatadas pelo usuário autenticado
    recompensas_resgatadas_ids = []
    if current_user.is_authenticated:
        recompensas_resgatadas_ids = [
            resgatada.codRecompensa for resgatada in current_user.recompensas_resgatadas
        ]

    return render_template(
        'recompensas.html',
        recompensas=recompensas,
        recompensas_resgatadas_ids=recompensas_resgatadas_ids,
        usuario_autenticado=current_user.is_authenticated
    )

# Rota para resgatar recompensas
@recompensas_route.route('/resgatar_recompensa', methods=['POST'])
def resgatar_recompensa():
    pontos_necessarios = request.form.get('pontos', '').strip()
    recompensa_id = request.form.get('recompensa_id', '').strip()

    if not pontos_necessarios or not recompensa_id:
        return redirect(url_for('recompensas.recompensas'))

    try:
        pontos_necessarios = int(pontos_necessarios)
        recompensa_id = int(recompensa_id)
    except ValueError:
        return redirect(url_for('recompensas.recompensas'))

    # Verifica se o usuário já resgatou a recompensa
    recompensa_resgatada = RecompensasResgatadas.query.filter_by(
        codUsuario=current_user.codigo, codRecompensa=recompensa_id).first()

    if recompensa_resgatada:
        return redirect(url_for('recompensas.recompensas'))

    if current_user.quantidadePontos >= pontos_necessarios:
        current_user.quantidadePontos -= pontos_necessarios

        nova_recompensa_resgatada = RecompensasResgatadas(
            codUsuario=current_user.codigo,
            codRecompensa=recompensa_id
        )
        db.session.add(nova_recompensa_resgatada)
        db.session.commit()

        return redirect(url_for('recompensas.recompensas'))

    # Caso pontos insuficientes
    return redirect(url_for('recompensas.recompensas', sucesso="recompensa_recusada"))

