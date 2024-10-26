from database.db import db
from datetime import datetime

class Pergunta(db.Model):
    __tablename__ = 'perguntas'
    
    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    codCategoria = db.Column(db.Integer, db.ForeignKey('categorias.codigo'), nullable=False)

    # Relacionamentos de tabelas
    categoria_relacionada = db.relationship('Categoria', backref='perguntas', lazy=True)
    usuario_relacionado = db.relationship('Usuario', backref='perguntas_usuario', lazy=True)
    notificacao_relacionada = db.relationship('Notificacao', back_populates='pergunta_relacionada', lazy=True)
    etiqueta_relacionada = db.relationship('PerguntasEtiquetas', backref='pergunta_rel', cascade='all, delete-orphan')
    etiquetas = db.relationship('Etiqueta', secondary='pergunta_etiqueta', backref='perguntas')

    def __repr__(self):
        return f'<Pergunta {self.titulo}>'