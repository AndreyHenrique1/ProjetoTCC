from database.db import db
from sqlalchemy.orm import relationship

class Categoria(db.Model):
    __tablename__ = 'categorias'

    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(255))

    def __repr__(self):
        return f'<Categoria {self.nome}>'
