from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models.denuncia import Denuncia
from models.comentariosPerguntas import comentariosPerguntas
from database.db import db

denuncia_route = Blueprint('denuncia_route', __name__)

# Rota para enviar uma denúncia de comentário
@denuncia_route.route('/denunciar/comentario/<int:comentario_id>', methods=['GET', 'POST'])
@login_required
def denunciar(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)
    
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        
        # Verifica se já existe uma denúncia para este comentário por este usuário
        existing_denuncia = Denuncia.query.filter_by(codComentario=comentario_id, codUsuario=current_user.codigo).first()
        if existing_denuncia:
            flash('Você já denunciou este comentário.', 'warning')
            return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta))
        
        # Cria uma nova denúncia
        nova_denuncia = Denuncia(codComentario=comentario_id, codPergunta=comentario.codPergunta, codUsuario=current_user.codigo, descricao=descricao)
        db.session.add(nova_denuncia)
        db.session.commit()
        
        flash('Denúncia enviada com sucesso!', 'success')
        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta))
    
    return render_template('detalhes_pergunta.html', comentario=comentario)

# Rota para ver as denúncias de um comentário específico
@denuncia_route.route('/denuncias/comentario/<int:comentario_id>')
@login_required
def ver_denuncias(comentario_id):
    denuncias = Denuncia.query.filter_by(codComentario=comentario_id).all()
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)
    return render_template('ver_denuncias.html', denuncias=denuncias, comentario=comentario)

