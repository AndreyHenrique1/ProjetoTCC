from database.db import db
from datetime import datetime
from models.likes_deslikes import Likes_deslikes

class comentariosPerguntas(db.Model):
    __tablename__ = 'comentariosperguntas'
    
    codigo = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(1000), nullable=False)
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    quantidadeCurtidas = db.Column(db.Integer, default=0)  # quantidade total de curtidas (likes)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    melhor_resposta = db.Column(db.Boolean, default=False)

    # Relacionamentos de tabelas
    usuario_relacionado = db.relationship('Usuario', backref='comentariosPerguntas', lazy=True)
    pergunta_relacionada = db.relationship('Pergunta', backref='comentarios', lazy=True)
    denuncia_relacionada = db.relationship('Denuncia', backref='comentario', lazy=True)
    likes_relacionados = db.relationship('Likes_deslikes', backref='likes_comentario', lazy=True)

    # Contagem de likes
    @property
    def quantidade_likes(self):
        return Likes_deslikes.query.filter_by(codComentarioPergunta=self.codigo, tipo='like').count()

    # Contagem de deslikes
    @property
    def quantidade_deslikes(self):
        return Likes_deslikes.query.filter_by(codComentarioPergunta=self.codigo, tipo='deslike').count()

    def __repr__(self):
        return f'<comentariosPerguntas {self.codigo}>'


