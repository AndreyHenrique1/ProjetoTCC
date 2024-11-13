from database.db import db

class CurtidasComentarios(db.Model):
    __tablename__ = 'curtidas_comentarios'
    codigo = db.Column(db.Integer, primary_key=True)
    codComentario = db.Column(db.Integer, db.ForeignKey('comentariosperguntas.codigo'), nullable=False)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)

    def __init__(self, codComentario, codUsuario):
        self.codComentario = codComentario
        self.codUsuario = codUsuario
