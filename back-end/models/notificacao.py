from database.db import db
from datetime import datetime

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'

    codigo = db.Column(db.Integer, primary_key=True)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    mensagem = db.Column(db.String(255), nullable=False)
    link_pergunta = db.Column(db.String(255), nullable=True)
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=True)
    codBlog = db.Column(db.Integer, db.ForeignKey('blog.codigo'), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)

    # Relacionamentos
    pergunta_relacionada = db.relationship('Pergunta', backref='notificacoes', foreign_keys=[codPergunta])
    blog_relacionado = db.relationship('Blog', backref='notificacoes', foreign_keys=[codBlog])


    def __repr__(self):
        return f'<Notificacao {self.codigo}>'

def enviar_notificacao(codUsuario, mensagem, link_pergunta, codBlog=None, codPergunta=None):
    if codBlog is not None and codPergunta is None:  # Para notificação de blog
        notificacao = Notificacao(
            codUsuario=codUsuario,
            mensagem=mensagem,
            link_pergunta=link_pergunta,
            codBlog=codBlog,  # Preenche codBlog
            codPergunta=None,  # Deixa codPergunta como None
            data_criacao=datetime.utcnow(),
            lida=False
        )
    elif codPergunta is not None and codBlog is None:  # Para notificação de pergunta
        notificacao = Notificacao(
            codUsuario=codUsuario,
            mensagem=mensagem,
            link_pergunta=link_pergunta,
            codPergunta=codPergunta,  # Preenche codPergunta
            codBlog=None,  # Deixa codBlog como None
            data_criacao=datetime.utcnow(),
            lida=False
        )
    else:
        raise ValueError("Deve ser fornecido apenas um entre codBlog ou codPergunta.")
    
    db.session.add(notificacao)
    db.session.commit()

