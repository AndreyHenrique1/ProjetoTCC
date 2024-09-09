from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Resposta(db.Model):
    __tablename__ = 'respostas'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(1000), nullable=False)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='respostas', lazy=True)
