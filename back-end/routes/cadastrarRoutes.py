from flask import render_template, Blueprint, request, redirect, url_for, flash
from models.usuario import Usuario
from database.db import db
import random, base64
from io import BytesIO

cadastrar_route = Blueprint('cadastrar_route', __name__)

# Rota para cadastrar novos usuários
@cadastrar_route.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        email = request.form['email']
        nomeCompleto = request.form.get('nomeCompleto')
        nomeUsuario = request.form['nomeUsuario']
        senha = request.form['senha']

        # Verificação de usuário existente
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Esse e-mail já está cadastrado.', 'danger')
            return redirect(url_for('cadastrar_route.cadastrar'))
        
        usuario_existente_nome = Usuario.query.filter_by(nomeUsuario=nomeUsuario).first()
        if usuario_existente_nome:
            flash('Esse nome de usuário já está sendo usado. Escolha outro.', 'danger')
            return redirect(url_for('cadastrar_route.cadastrar'))

        # Geração do avatar e da cor aleatória
        inicial = nomeUsuario[0].upper()  # Pega a primeira letra do nome de usuário
        cor_avatar = gerar_cor_aleatoria()  # Gera uma cor aleatória
        foto_perfil = gerar_avatar_svg(cor_avatar, inicial)  # Gera o avatar SVG

        # Adiciona o novo usuário ao banco de dados
        usuario = Usuario(email=email, nomeCompleto=nomeCompleto, nomeUsuario=nomeUsuario, senha=senha, foto_perfil=foto_perfil, cor_avatar=cor_avatar)
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for('login_route.login'))

    return render_template("cadastrar_usuario.html")

# Rota para verificar usuário
@cadastrar_route.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    nomeUsuario = request.json.get('nomeUsuario')
    usuario_existente = Usuario.query.filter_by(nomeUsuario=nomeUsuario).first()
    if usuario_existente:
        return {'existe': True}
    return {'existe': False}

# Função para gerar uma cor aleatória
def gerar_cor_aleatoria():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Função para gerar o SVG do avatar
def gerar_avatar_svg(cor, inicial):
    svg_content = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="150" height="150">
        <rect width="100%" height="100%" fill="{cor}" rx="20" />
        <text x="50%" y="50%" font-size="60" text-anchor="middle" fill="#FFFFFF" dy=".3em">{inicial}</text>
    </svg>
    '''
    # Codifica o SVG para base64
    svg_bytes = BytesIO(svg_content.encode('utf-8'))
    svg_base64 = base64.b64encode(svg_bytes.getvalue()).decode('utf-8')
    return f"data:image/svg+xml;base64,{svg_base64}"
