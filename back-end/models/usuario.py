from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import login_manager
from sqlalchemy.orm import relationship
import random
import base64

# Carrega o usuário logado
@login_manager.user_loader
def get_user(usuario_id):
    return Usuario.query.filter_by(codigo=usuario_id).first()

class Usuario(db.Model, UserMixin):
    codigo = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nomeCompleto = db.Column(db.String(50))
    nomeUsuario = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    quantidadePontos = db.Column(db.Integer, default=0)
    foto_perfil = db.Column(db.Text, nullable=True)  
    cor_avatar = db.Column(db.String(7), nullable=True)

    perguntas = relationship("Pergunta", back_populates="usuario")

    def __init__(self, email, nomeCompleto, nomeUsuario, senha, foto_perfil=None, quantidadePontos=0, cor_avatar=None):
        self.email = email
        self.nomeCompleto = nomeCompleto
        self.nomeUsuario = nomeUsuario
        self.senha = generate_password_hash(senha)
        self.foto_perfil = foto_perfil  
        self.quantidadePontos = quantidadePontos
        self.cor_avatar = cor_avatar
    
    # Método para verificar a senha
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def get_id(self):
        return str(self.codigo)

    # Retorna um dicionário com as informações do usuário
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'email': self.email,
            'nomeCompleto': self.nomeCompleto,
            'nomeUsuario': self.nomeUsuario,
            'quantidadePontos': self.quantidadePontos,
            'foto_perfil': self.foto_perfil,
            'cor_avatar': self.cor_avatar
        }
    

