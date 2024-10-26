from database.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class comentariosBlog(db.Model):
    __tablename__ = 'comentariosblog'
    
    codigo = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(1000), nullable=False)
    codBlog = db.Column(db.Integer, db.ForeignKey('blog.codigo'), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)

    # Relacionamentos de tabelas
    usuario_relacionado = db.relationship('Usuario', backref='comentariosBlog', lazy=True)
    blog_relacionado = db.relationship('Blog', backref='comentarios', lazy=True)

    def __repr__(self):
        return f'<ComentarioBlog {self.codigo}>'
