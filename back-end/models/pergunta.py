from database.db import db
from datetime import datetime

class Pergunta(db.Model):
    __tablename__ = 'perguntas'
    
    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)  # Corrigido: nome correto do campo de referência
    codCategoria = db.Column(db.Integer, db.ForeignKey('categorias.codigo'), nullable=False)  # Corrigido: referenciando 'categorias.codigo'

    # Relacionamentos
    categoria_relacionado = db.relationship('Categoria', backref='perguntas')
    
    usuario = db.relationship('Usuario', backref='perguntas_usuario', lazy=True)

    notificacoes = db.relationship('Notificacao', back_populates='pergunta_relacionada')

    etiquetas = db.relationship('PerguntasEtiquetas', backref='pergunta_rel', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pergunta {self.titulo}>'
