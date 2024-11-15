from database.db import db
from sqlalchemy.orm import relationship

class Etiqueta(db.Model):
    __tablename__ = 'etiquetas'
    
    codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    popularidade = db.Column(db.Integer, default=0)

    # Relacionamento com a tabela de associação
    pergunta_relacionada = db.relationship('PerguntasEtiquetas', backref='etiqueta_ref', lazy=True)
    blog = db.relationship('Blog', secondary='blog_etiqueta', backref=db.backref('etiquetas', lazy='dynamic'))

    def __repr__(self):
        return f'<Etiqueta {self.nome}>'
