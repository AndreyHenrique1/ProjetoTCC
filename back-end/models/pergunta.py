from database.db import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Pergunta(db.Model):
    __tablename__ = 'perguntas'
    
    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    codCategoria = db.Column(db.Integer, db.ForeignKey('categorias.codigo'), nullable=False)

    # Relacionamentos
    categoria_relacionado = db.relationship('Categoria', backref='perguntas')
    
    # Renomeado o backref para evitar conflito
    usuario = db.relationship('Usuario', backref='perguntas_usuario', lazy=True)

    # Relacionamento com notificações
    notificacoes = db.relationship('Notificacao', back_populates='pergunta_relacionada')

    # Relacionamento com PerguntasEtiquetas
    etiquetas = db.relationship('PerguntasEtiquetas', backref='pergunta_rel', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pergunta {self.titulo}>'
