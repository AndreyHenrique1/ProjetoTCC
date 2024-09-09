from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class comentariosPerguntas(db.Model):
    __tablename__ = 'comentariosperguntas'
    codigo = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(1000), nullable=False)
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)

    # Relacionamento com a tabela Usuário 
    usuario_relacionado = db.relationship('Usuario', backref='cometariosPerguntas', lazy=True)
    pergunta_relacionado = db.relationship('Pergunta', backref='perguntas', lazy=True)
