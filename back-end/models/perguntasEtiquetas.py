from database.db import db

class PerguntasEtiquetas(db.Model):
    __tablename__ = 'pergunta_etiqueta'
    
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), primary_key=True)
    codEtiqueta = db.Column(db.Integer, db.ForeignKey('etiquetas.codigo'), primary_key=True)

    # Relacionamentos de tabelas
    pergunta_relacionada = db.relationship('Pergunta', backref='perguntasEtiquetas', lazy=True)
    etiqueta_relacionada = db.relationship('Etiqueta', backref='perguntasEtiquetas', lazy=True)