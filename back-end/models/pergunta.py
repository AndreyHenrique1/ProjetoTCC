from database.db import db
from datetime import datetime

class Pergunta(db.Model):
    __tablename__ = 'perguntas'

    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    codusuario = db.Column(db.Integer, default=1)  
    codCategoria = db.Column(db.Integer, default=1)  

    def __repr__(self):
        return f'<Pergunta {self.titulo}>'
