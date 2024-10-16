from database.db import db

class PerguntasEtiquetas(db.Model):
    __tablename__ = 'pergunta_etiqueta'
    
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), primary_key=True)
    codEtiqueta = db.Column(db.Integer, db.ForeignKey('etiquetas.codigo'), primary_key=True)

    # Relações
    pergunta = db.relationship('Pergunta', backref='perguntasEtiquetas', lazy=True)
    etiqueta = db.relationship('Etiqueta', backref='perguntasEtiquetas', lazy=True)

    def __repr__(self):
        return f'<pergunta_etiqueta {self.codPergunta}, {self.codEtiqueta}>'
