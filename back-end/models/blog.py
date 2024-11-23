from database.db import db
from datetime import datetime
from models.likes_deslikes import Likes_deslikes

class Blog(db.Model):
    __tablename__ = 'blog'

    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(10000), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    codCategoria = db.Column(db.Integer, db.ForeignKey('categorias.codigo'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    fotoCapa_blog = db.Column(db.Text, nullable=True)
    quantidadeCurtidas = db.Column(db.Integer, default=0)

    # Relacionamentos de tabelas
    usuario_relacionado = db.relationship('Usuario', back_populates='blog_relacionado')
    categoria_relacionada = db.relationship('Categoria', backref='blogs', lazy=True)
    denuncia_relacionada = db.relationship('Denuncia', backref='blogs', lazy=True)
    etiqueta = db.relationship('Etiqueta', secondary='blog_etiqueta', backref=db.backref('blogs', lazy='dynamic'))

    # Propriedade para contar likes
    @property
    def quantidade_likes(self):
        return Likes_deslikes.query.filter_by(codBlog=self.codigo, tipo='like', origem='blog').count()

    # Propriedade para contar deslikes
    @property
    def quantidade_deslikes(self):
        return Likes_deslikes.query.filter_by(codBlog=self.codigo, tipo='deslike', origem='blog').count()

    def __repr__(self):
        return f'<Blog {self.titulo}>'
