from database.db import db

class Categoria(db.Model):
    __tablename__ = 'categorias'  

    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    cor = db.Column(db.String(7), nullable=True)  

    def __repr__(self):
        return f'<Categoria {self.nome}>'
