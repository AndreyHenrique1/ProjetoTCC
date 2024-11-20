from database.db import db

class Recompensa(db.Model):
    __tablename__ = 'recompensas'
    
    codigo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=True)
    pontos = db.Column(db.Integer, nullable=False)

    # Relacionamento com a tabela 'RecompensasResgatadas'
    recompensas_resgatadas = db.relationship('RecompensasResgatadas', back_populates='recompensa')

    def __repr__(self):
        return f'<Recompensa {self.descricao}>'

