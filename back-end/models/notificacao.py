from database.db import db
from datetime import datetime

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    
    codigo = db.Column(db.Integer, primary_key=True)
    codUsuario = db.Column(db.Integer, db.ForeignKey('usuario.codigo'), nullable=False)
    mensagem = db.Column(db.String(255), nullable=False)
    link_pergunta = db.Column(db.String(255), nullable=True)
    codPergunta = db.Column(db.Integer, db.ForeignKey('perguntas.codigo'), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)

    # Relacionamentos de tabelas
    usuario_relacionado = db.relationship('Usuario', back_populates='notificacao_relacionada')
    pergunta_relacionada = db.relationship('Pergunta', back_populates='notificacao_relacionada')

    def __repr__(self):
        return f'<Notificacao {self.codigo}>'

# Função para enviar a notificação
def enviar_notificacao(codUsuario, mensagem, link_pergunta=None, codPergunta=None):
    nova_notificacao = Notificacao(codUsuario=codUsuario, mensagem=mensagem, link_pergunta=link_pergunta, codPergunta=codPergunta)
    db.session.add(nova_notificacao)
    db.session.commit()
