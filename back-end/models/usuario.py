from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    codigo = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    nomeCompleto = db.Column(db.String(50))
    nomeUsuario = db.Column(db.String(50), nullable=True)
    senha = db.Column(db.String(100), nullable=True)  
    quantidadePontos = db.Column(db.Integer, default=0)  

    def __init__(self, email, nomeCompleto, nomeUsuario, senha, quantidadePontos=0):
        self.email = email
        self.nomeCompleto = nomeCompleto
        self.nomeUsuario = nomeUsuario
        self.senha = generate_password_hash(senha)
        self.quantidadePontos = quantidadePontos

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def to_dict(self):
        return {
            'codigo': self.codigo,
            'email': self.email,
            'nomeCompleto': self.nomeCompleto,
            'nomeUsuario': self.nomeUsuario,
            'senha': self.senha,
            'quantidadePontos': self.quantidadePontos
        }
