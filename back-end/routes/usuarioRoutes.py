from io import BytesIO
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from database.db import db
from models.usuario import Usuario
from models.pergunta import Pergunta
from models.blog import Blog
from models.perguntasEtiquetas import PerguntasEtiquetas
from models.etiqueta import Etiqueta
from models.comentariosPerguntas import comentariosPerguntas
from models.denuncia import Denuncia
from models.recompensas import Recompensa
from models.recompensasResgatadas import RecompensasResgatadas
import cloudinary.uploader
from models.notificacao import enviar_notificacao
from collections import Counter
from sqlalchemy import desc

usuario_route = Blueprint('usuario_route', __name__)

# Função para obter o ranking e a medalha correspondente
def obter_ranking_e_medalha(user_id):
    usuarios = Usuario.query.order_by(Usuario.quantidadePontos.desc()).all()  # Ordena todos os usuários
    for posicao, usuario in enumerate(usuarios, start=1):
        if usuario.codigo == user_id:
            if posicao == 1:
                medalha = {"cor": "gold", "numero": posicao}
            elif posicao == 2:
                medalha = {"cor": "silver", "numero": posicao}
            elif posicao == 3:
                medalha = {"cor": "bronze", "numero": posicao}
            else:
                medalha = {"cor": "black", "numero": posicao}
            return posicao, medalha
    return None, None

@usuario_route.route('/perfil')
@login_required
def perfil():
    # Verifica se o usuário possui 300 pontos ou mais para se tornar moderador
    if current_user.quantidadePontos >= 300 and not current_user.moderador:
        current_user.moderador = True
        db.session.commit()
    
    else:
        current_user.moderador = False

    sobre_usuario = current_user.sobre
    tags_mais_usadas = obter_etiquetas_mais_usadas(current_user.codigo)

    perguntas = Pergunta.query.filter_by(codUsuario=current_user.codigo).all()
    blogs = Blog.query.filter_by(codUsuario=current_user.codigo).all()
    respostas = comentariosPerguntas.query.filter_by(codUsuario=current_user.codigo).all()

    # Contagem das atividades do usuário
    perguntas_count = Pergunta.query.filter_by(codUsuario=current_user.codigo).count()
    blogs_count = Blog.query.filter_by(codUsuario=current_user.codigo).count()
    respostas_count = comentariosPerguntas.query.filter_by(codUsuario=current_user.codigo).count()
    denuncias_count = Denuncia.query.filter_by(codUsuario=current_user.codigo).count()

    # Obtém o ranking e a medalha do usuário atual
    ranking, medalha = obter_ranking_e_medalha(current_user.codigo)

    return render_template(
        'perfil.html',
        perguntas=perguntas,
        blogs=blogs,
        respostas=respostas,
        perguntas_count=perguntas_count,
        blogs_count=blogs_count,
        respostas_count=respostas_count,
        denuncias_count=denuncias_count,
        sobre=sobre_usuario,
        ranking=ranking,
        medalha=medalha,
        etiquetas_mais_usadas=tags_mais_usadas,
        usuario=current_user, 
        moderador=current_user.moderador 
    )

# Rota para atualizar as novas atualizações de informações do usuário 
@usuario_route.route('/editar_perfil', methods=['POST'])
@login_required
def editar_perfil():
    novo_nome = request.form.get('nomeUsuario')
    sobre = request.form.get('sobre')

    # Atualiza o campo 'sobre' no banco de dados, se fornecido
    if sobre:
        current_user.sobre = sobre

    # Atualiza o nome de usuário, se fornecido
    if novo_nome:
        current_user.nomeUsuario = novo_nome

    # Verifica se uma imagem foi selecionada
    if 'imagem' in request.files and request.files['imagem'].filename != '':
        imagem = request.files['imagem']

        # Faz o upload da imagem para o Cloudinary e obtém a URL segura
        upload_result = cloudinary.uploader.upload(imagem, folder="fotos_perfil")
        url_imagem = upload_result.get('secure_url')

        # Atualiza o campo `foto_perfil` no banco de dados, se uma nova imagem foi enviada
        if url_imagem:
            current_user.foto_perfil = url_imagem

    db.session.commit()

    return redirect(url_for('usuario_route.perfil', sucesso="usuario_editado"))

# Rota da lista de usuários
@usuario_route.route('/usuarios')
def listar_usuarios():
    recompensas = Recompensa.query.all()  # Obter todas as recompensas do banco de dados
    search_query = request.args.get('search')  # Obtém o nome do usuário a partir da query string
    
    usuarios = Usuario.query.order_by(desc(Usuario.quantidadePontos)).all()  # Usuários ordenados por pontos

    # Obter IDs das recompensas já resgatadas pelo usuário autenticado
    recompensas_resgatadas_ids = []
    if current_user.is_authenticated:
        recompensas_resgatadas_ids = [
            resgatada.codRecompensa for resgatada in current_user.recompensas_resgatadas
        ]

    if search_query:
        usuarios = [usuario for usuario in usuarios if search_query.lower() in usuario.nomeUsuario.lower()]
    
    return render_template(
        'listar_usuarios.html',
        usuarios=usuarios,
        recompensas=recompensas,
        recompensas_resgatadas_ids=recompensas_resgatadas_ids,
        obter_ranking_e_medalha=obter_ranking_e_medalha,
        usuario_autenticado=current_user.is_authenticated
    )


# Função para obter as etiquetas mais usadas
def obter_etiquetas_mais_usadas(user_id):
    # Obter todas as perguntas do usuário
    perguntas = Pergunta.query.filter_by(codUsuario=user_id).all()
    
    # Coletar todas as etiquetas associadas a essas perguntas
    todas_etiquetas = []
    for pergunta in perguntas:
        # Obter os códigos de etiqueta associadas à pergunta
        etiquetas = PerguntasEtiquetas.query.filter_by(codPergunta=pergunta.codigo).all()
        todas_etiquetas.extend([tag.codEtiqueta for tag in etiquetas])
    
    # Contar as etiquetas
    contagem_etiquetas = Counter(todas_etiquetas)

    # Criar uma lista com as 5 etiquetas mais comuns
    etiquetas_mais_usadas = []
    for codEtiqueta, count in contagem_etiquetas.most_common(5):
        etiqueta = Etiqueta.query.get(codEtiqueta)  # Obter a etiqueta pelo código
        if etiqueta:
            etiquetas_mais_usadas.append((etiqueta.nome, count))  # Adicionar o nome da etiqueta e a contagem
    
    return etiquetas_mais_usadas

@usuario_route.route('/perfil/<int:user_id>')
def perfil_outro_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for('home.homePergunta'))
    
    # Obtendo informações do usuário que está sendo visualizado
    tags_mais_usadas = obter_etiquetas_mais_usadas(usuario.codigo)
    perguntas = Pergunta.query.filter_by(codUsuario=usuario.codigo).all()
    blogs = Blog.query.filter_by(codUsuario=usuario.codigo).all()
    respostas = comentariosPerguntas.query.filter_by(codUsuario=usuario.codigo).all()

    perguntas_count = Pergunta.query.filter_by(codUsuario=usuario.codigo).count()
    blogs_count = Blog.query.filter_by(codUsuario=usuario.codigo).count()
    respostas_count = comentariosPerguntas.query.filter_by(codUsuario=usuario.codigo).count()

    ranking, medalha = obter_ranking_e_medalha(usuario.codigo)

    return render_template(
        'perfil.html',
        usuario=usuario,
        perguntas=perguntas,
        blogs=blogs,
        respostas=respostas,
        perguntas_count=perguntas_count,
        blogs_count=blogs_count,
        respostas_count=respostas_count,
        ranking=ranking,
        medalha=medalha,
        etiquetas_mais_usadas=tags_mais_usadas
    )

@usuario_route.route('/resgatar_recompensa', methods=['POST'])
def resgatar_recompensa():
    pontos_necessarios = request.form.get('pontos', '').strip()
    recompensa_id = request.form.get('recompensa_id', '').strip()

    if not pontos_necessarios or not recompensa_id:
        flash('Dados inválidos ou incompletos.', 'error')
        return redirect(url_for('usuario_route.listar_usuarios'))

    try:
        pontos_necessarios = int(pontos_necessarios)
        recompensa_id = int(recompensa_id)
    except ValueError:
        flash('Erro ao processar os dados. Tente novamente.', 'error')
        return redirect(url_for('usuario_route.listar_usuarios'))

    # Verifica se o usuário já resgatou a recompensa
    recompensa_resgatada = RecompensasResgatadas.query.filter_by(
        codUsuario=current_user.codigo, codRecompensa=recompensa_id).first()

    if recompensa_resgatada:
        flash('Você já resgatou essa recompensa.', 'warning')
        return redirect(url_for('usuario_route.listar_usuarios'))

    if current_user.quantidadePontos >= pontos_necessarios:
        current_user.quantidadePontos -= pontos_necessarios

        nova_recompensa_resgatada = RecompensasResgatadas(
            codUsuario=current_user.codigo,
            codRecompensa=recompensa_id
        )
        db.session.add(nova_recompensa_resgatada)
        db.session.commit()

        return redirect(url_for('usuario_route.listar_usuarios', sucesso="recompesa_resgatada"))

    return redirect(url_for('usuario_route.listar_usuarios', recompensa_resgatada=recompensa_resgatada))
