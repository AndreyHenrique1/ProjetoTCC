from database.db import db
from datetime import datetime

class Blog(db.Model):
    __tablename__ = 'blog'

    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(10000), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    codCategoria = db.Column(db.Integer, db.ForeignKey('categorias.codigo'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com usuário e categoria
    usuario_relacionado = db.relationship('Usuario', backref='blogs', lazy=True)
    categoria_relacionada = db.relationship('Categoria', backref='blogs', lazy=True)
