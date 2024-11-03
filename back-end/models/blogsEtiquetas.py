from database.db import db

class BlogsEtiquetas(db.Model):
    __tablename__ = 'blog_etiqueta'
    
    codBlog = db.Column(db.Integer, db.ForeignKey('blog.codigo'), primary_key=True)
    codEtiqueta = db.Column(db.Integer, db.ForeignKey('etiquetas.codigo'), primary_key=True)

    # Relacionamentos de tabelas
    blog_relacionada = db.relationship('Blog', backref='blogsEtiquetas', lazy=True)
    etiqueta_relacionada = db.relationship('Etiqueta', backref='blogsEtiquetas', lazy=True)

    def __repr__(self):
        return f'<BlogsEtiquetas {self.codBlog}, {self.codEtiqueta}>'