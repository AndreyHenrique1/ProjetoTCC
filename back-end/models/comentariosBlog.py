from database.db import db
from datetime import datetime
from models.likes_deslikes import Likes_deslikes

class comentariosBlog(db.Model):
    __tablename__ = 'comentariosblog'
    
    codigo = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(1000), nullable=False)
    codBlog = db.Column(db.Integer, db.ForeignKey('blog.codigo'), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    quantidadeCurtidas = db.Column(db.Integer, default=0)

    # Relacionamentos de tabelas
    usuario_relacionado = db.relationship('Usuario', backref='comentariosBlog', lazy=True)
    blog_relacionado = db.relationship('Blog', backref='comentarios', lazy=True)

    # Contagem de likes
    @property
    def quantidade_likes(self):
        return Likes_deslikes.query.filter_by(codComentarioBlog=self.codigo, tipo='like').count()

    # Contagem de deslikes
    @property
    def quantidade_deslikes(self):
        return Likes_deslikes.query.filter_by(codComentarioBlog=self.codigo, tipo='deslike').count()

    def __repr__(self):
        return f'<ComentarioBlog {self.codigo}>'

