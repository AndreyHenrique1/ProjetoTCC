from database.db import db
from datetime import datetime

class Denuncia(db.Model):
    __tablename__ = 'denuncias'
    
    codigo = db.Column(db.Integer, primary_key=True)
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=True)
    codComentario = db.Column(db.Integer, db.ForeignKey('comentariosperguntas.codigo'), nullable=True)
    codBlog = db.Column(db.Integer, db.ForeignKey('blog.codigo'), nullable=True)  
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    verificada = db.Column(db.Boolean, default=False)

    # Relacionamentos
    pergunta_relacionada = db.relationship('Pergunta', backref='denuncias', lazy=True)
    usuario_relacionado = db.relationship('Usuario', backref='denuncias', lazy=True)
    comentario_relacionado = db.relationship('comentariosPerguntas', backref='denuncias', lazy=True)
    blog_relacionado = db.relationship('Blog', backref='denuncias', lazy=True)  

    def __repr__(self):
        return f'<Denuncia {self.codigo}>'
