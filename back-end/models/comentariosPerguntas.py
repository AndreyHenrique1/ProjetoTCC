from database.db import db
from sqlalchemy.orm import relationship
from datetime import datetime

class comentariosPerguntas(db.Model):
    __tablename__ = 'comentariosperguntas'
    
    codigo = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(1000), nullable=False)
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    quantidadeCurtidas = db.Column(db.Integer, default=0) 
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos de tabelas
    usuario_relacionado = db.relationship('Usuario', backref='comentariosPerguntas', lazy=True)
    pergunta_relacionada = db.relationship('Pergunta', backref='comentarios', lazy=True)
    denuncia_relacionada = db.relationship('Denuncia', backref='comentario', lazy=True)


    def __repr__(self):
        return f'<comentariosPerguntas {self.codigo}>'
    
