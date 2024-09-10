from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Pergunta(db.Model):
    __tablename__ = 'perguntas'
    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    descrição = db.Column(db.String(1000), nullable=False) 
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    codCategoria = db.Column(db.Integer, db.ForeignKey('categorias.codigo'), nullable=False)


    # Relacionamento com a tabela Categoria e Usuário
    categoria_relacionado = relationship('Categoria', backref='perguntas')
    usuario_relacionado = relationship('Usuario', backref='usuario')

    def __repr__(self):
        return f'<Pergunta {self.titulo}>'
