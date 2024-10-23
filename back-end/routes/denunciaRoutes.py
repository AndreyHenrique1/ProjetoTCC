from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models.denuncia import Denuncia
from models.pergunta import Pergunta
from database.db import db

denuncia_route = Blueprint('denuncia_route', __name__)

# Rota para enviar uma denúncia
@denuncia_route.route('/denunciar/<int:pergunta_id>', methods=['GET', 'POST'])
@login_required
def denunciar(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        
        # Cria uma nova denúncia
        nova_denuncia = Denuncia(codPergunta=pergunta_id, codUsuario=current_user.codigo, descricao=descricao)
        db.session.add(nova_denuncia)
        db.session.commit()
        
        flash('Denúncia enviada com sucesso.', 'success')
        return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=pergunta_id))
    
    return render_template('denunciar_pergunta.html', pergunta=pergunta)
