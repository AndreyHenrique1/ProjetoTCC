from database.db import db
from sqlalchemy.orm import relationship

class comentariosPerguntas(db.Model):
    __tablename__ = 'comentariosperguntas'
    codigo = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(1000), nullable=False)
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    quantidadeCurtidas = db.Column(db.Integer, default=0)

    # Relacionamento com a tabela Usuário 
    usuario_relacionado = db.relationship('Usuario', backref='comentarios', lazy=True)
    
    # Relacionamento com a pergunta
    pergunta_relacionado = db.relationship('Pergunta', backref='comentarios', lazy=True)
