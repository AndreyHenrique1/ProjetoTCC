from database.db import db
from datetime import datetime

class Denuncia(db.Model):
    __tablename__ = 'denuncias'
    codigo = db.Column(db.Integer, primary_key=True)
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com perguntas e usuários
    pergunta_relacionada = db.relationship('Pergunta', backref='denuncias', lazy=True)
    usuario_relacionado = db.relationship('Usuario', backref='denuncias', lazy=True)
