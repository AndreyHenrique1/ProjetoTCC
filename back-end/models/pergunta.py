from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Pergunta(db.Model):
    __tablename__ = 'perguntas'

    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    codUsuario = db.Column(db.Integer, ForeignKey('usuario.codigo'))
    codCategoria = db.Column(db.Integer, ForeignKey('categorias.codigo'))  

    # Relacionamento com a tabela Categoria
    categoria_relacionado = relationship('Categoria', backref='perguntas')
    usuario_relacionado = relationship('Usuario', backref='usuario')

    def __repr__(self):
        return f'<Pergunta {self.titulo}>'
