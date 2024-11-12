# Certifique-se de que a classe 'ComentariosPerguntas' está definida corretamente antes de ser usada.
from database.db import db
from datetime import datetime

class Likes_deslikes(db.Model):
    __tablename__ = 'likes_deslikes'

    codigo = db.Column(db.Integer, primary_key=True)
    codComentarioPergunta = db.Column(db.Integer, db.ForeignKey('comentariosperguntas.codigo'))
    codComentarioBlog = db.Column(db.Integer, db.ForeignKey('comentariosblog.codigo'))
    codBlog = db.Column(db.Integer, db.ForeignKey('blog.codigo'))
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'))
    tipo = db.Column(db.Enum('like', 'deslike', name='like_type'), nullable=False)
    origem = db.Column(db.Enum('comentario_pergunta', 'comentario_blog', 'blog', name='origem_type'), nullable=False)
    data = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    # Relacionamentos com tabelas
    comentario_pergunta = db.relationship('comentariosPerguntas', backref='likes_relacionados_comentarios', lazy=True)
    comentario_blog = db.relationship('comentariosBlog', backref='likes_relacionados_blog', lazy=True)
    blog = db.relationship('Blog', backref='likes_relacionados_blog', lazy=True)
    usuario = db.relationship('Usuario', backref='likes_relacionados_usuario', lazy=True)

    def __repr__(self):
        return f'<Likes_deslikes {self.codigo}>'
