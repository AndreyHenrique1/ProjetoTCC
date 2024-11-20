from datetime import datetime
from database.db import db

class RecompensasResgatadas(db.Model):
    __tablename__ = 'recompensas_resgatadas'
    
    codigo = db.Column(db.Integer, primary_key=True)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'))  
    codRecompensa = db.Column(db.Integer, db.ForeignKey('recompensas.codigo'))  
    data_resgate = db.Column(db.DateTime, default=datetime.utcnow)  

    # Relacionamento com as tabelas 'Usuario' e 'Recompensa'
    usuario = db.relationship('Usuario', back_populates='recompensas_resgatadas')
    recompensa = db.relationship('Recompensa', back_populates='recompensas_resgatadas')

    def __repr__(self):
        return f'<RecompensaResgatada {self.codigo}>'
