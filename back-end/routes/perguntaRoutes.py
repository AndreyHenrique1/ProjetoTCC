from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database.db import db
from models.pergunta import Pergunta
from models.comentariosPerguntas import comentariosPerguntas
from models.categoria import Categoria
from models.etiqueta import Etiqueta
from models.likes_deslikes import Likes_deslikes
from models.denuncia import Denuncia
from models.usuario import Usuario
from models.notificacao import Notificacao
from models.perguntasEtiquetas import PerguntasEtiquetas
from models.notificacao import enviar_notificacao
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

pergunta_route = Blueprint('pergunta_route', __name__)

@pergunta_route.route('/perguntar', methods=['GET', 'POST'])
@login_required
def perguntar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        codCategoria = request.form['categorias']
        etiquetas_input = request.form['Etiqueta']
        codUsuario = current_user.codigo

        # Separando as etiquetas por # e removendo espaços 
        etiquetas_lista = [et.strip().lstrip('#') for et in etiquetas_input.split('#') if et.strip()]

        # Adiciona a pergunta no banco de dados
        nova_pergunta = Pergunta(titulo=titulo, descricao=descricao, codCategoria=codCategoria, codUsuario=codUsuario)
        db.session.add(nova_pergunta)

        # Adicionar etiquetas à pergunta
        for nome_etiqueta in etiquetas_lista:
            etiqueta_objeto = Etiqueta.query.filter_by(nome=nome_etiqueta).first()
            if etiqueta_objeto:
                etiqueta_objeto.popularidade += 1
            else:
                etiqueta_objeto = Etiqueta(nome=nome_etiqueta, popularidade=1)
                db.session.add(etiqueta_objeto)
            
            # Adicionando a associação PerguntasEtiquetas
            nova_pergunta_etiqueta = PerguntasEtiquetas(codPergunta=nova_pergunta.codigo, codEtiqueta=etiqueta_objeto.codigo)
            db.session.add(nova_pergunta_etiqueta)

        # Commit para salvar pergunta e etiquetas associadas
        db.session.commit()

        # Atualizando a quantidade de pontos do dono da pergunta (dando 3 pontos)
        dono_pergunta = Usuario.query.get(nova_pergunta.codUsuario)  # Obtém o dono da pergunta
        if dono_pergunta:  # Verifica se o dono da pergunta existe
            dono_pergunta.quantidadePontos += 3  # Adiciona 3 pontos ao dono da pergunta
            db.session.commit()

        # Retorna para a página de detalhes da pergunta com as etiquetas atualizadas
        return redirect(url_for('home.homePergunta', pergunta_id=nova_pergunta.codigo, sucesso="pergunta_enviada"))

    # Carregar todas as etiquetas para exibição no formulário
    etiquetas = Etiqueta.query.all()
    categorias = Categoria.query.all()

    return render_template('criar_pergunta.html', categorias=categorias, etiquetas=etiquetas)

# Rota de detalhes da pergunta
@pergunta_route.route('/pergunta/<int:pergunta_id>', methods=['GET'])
def detalhes_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    comentarios = comentariosPerguntas.query.filter_by(codPergunta=pergunta_id).all()
    return render_template('detalhes_pergunta.html', pergunta=pergunta, comentarios=comentarios)

# Rota para editar as perguntas
@pergunta_route.route('/pergunta/<int:pergunta_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    
    # Caso a pergunta não seja associada ao usuário, a pergunta não poderá ser editada
    if pergunta.codUsuario != current_user.codigo:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        pergunta.titulo = request.form['titulo']
        pergunta.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=pergunta_id, sucesso="pergunta_editada"))

# Rota para excluir pergunta
@pergunta_route.route('/pergunta/<int:pergunta_id>/excluir', methods=['POST'])
@login_required
def excluir_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    
    # Caso a pergunta não seja associada ao usuário, a pergunta não poderá ser excluída
    if pergunta.codUsuario != current_user.codigo:
        return redirect(url_for('home.homePergunta'))

    # Atualizando a quantidade de pontos do dono da pergunta (dando 3 pontos)
    dono_pergunta = Usuario.query.get(pergunta.codUsuario)  # Obtém o dono da pergunta
    if dono_pergunta:  # Verifica se o dono da pergunta existe
        dono_pergunta.quantidadePontos -= 3  # Retira 3 pontos do dono da pergunta
        db.session.commit()

    # Obter todas as notificações associadas à pergunta
    notificacoes = Notificacao.query.filter_by(codPergunta=pergunta.codigo).all()

    # Excluir ou atualizar notificações
    for notificacao in notificacoes:
        db.session.delete(notificacao)

    # Comita as mudanças para as notificações
    db.session.commit()

    # Obter todas as etiquetas associadas à pergunta
    etiquetas_associadas = PerguntasEtiquetas.query.filter_by(codPergunta=pergunta.codigo).all()

    # Excluir todas as associações que possuem na tabela PerguntasEtiquetas
    for associacao in etiquetas_associadas:
        # Verifica se a etiqueta ainda está associada a outras perguntas
        etiqueta = Etiqueta.query.get(associacao.codEtiqueta)
        
        if etiqueta:
            # Diminui a popularidade
            etiqueta.popularidade -= 1
            
            # Verifica se a popularidade é igual a 0, ou seja, não possui nenhum usuário com essa etiqueta
            if etiqueta.popularidade == 0:
                # Se não estiver associada a outras perguntas, exclui a etiqueta
                if not PerguntasEtiquetas.query.filter(PerguntasEtiquetas.codEtiqueta == etiqueta.codigo).filter(PerguntasEtiquetas.codPergunta != pergunta.codigo).first():
                    db.session.delete(etiqueta)

        # Exclui a associação da PerguntasEtiquetas
        db.session.delete(associacao)

    # Comita as mudanças para as associações e etiquetas processadas
    db.session.commit()

    # Excluir todas as denúncias relacionadas aos comentários da pergunta
    denuncias = Denuncia.query.filter_by(codPergunta=pergunta.codigo).all()
    for denuncia in denuncias:
        db.session.delete(denuncia)

    # Excluir todos os comentários relacionados à pergunta
    comentarios = comentariosPerguntas.query.filter_by(codPergunta=pergunta.codigo).all()
    for comentario in comentarios:
        # Exclui as denúncias associadas ao comentário, se existirem
        denuncias_comentario = Denuncia.query.filter_by(codComentario=comentario.codigo).all()
        for denuncia in denuncias_comentario:
            db.session.delete(denuncia)

        # Exclui o comentário
        db.session.delete(comentario)

    # Comita as mudanças para as denúncias e comentários processados
    db.session.commit()

    # Excluir a pergunta
    db.session.delete(pergunta)
    db.session.commit()
    
    return redirect(url_for('home.homePergunta', sucesso="pergunta_excluida"))

# Comentario da pergunta
@pergunta_route.route('/pergunta/<int:pergunta_id>', methods=['GET', 'POST'])
def comentarios_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)

    if request.method == 'POST':
        conteudo_comentario = request.form.get('conteudo_comentario')

        # Verificar se o conteúdo do comentário foi fornecido e se o usuário está autenticado
        if conteudo_comentario and current_user.is_authenticated:
            novo_comentario = comentariosPerguntas(
                comentario=conteudo_comentario, codPergunta=pergunta_id, codUsuario=current_user.codigo
            )
            db.session.add(novo_comentario)
            db.session.commit()

            # Aumentar 1 ponto para o dono do comentário
            usuario_comentario = Usuario.query.get(current_user.codigo)  # Pega o usuário que fez o comentário
            if usuario_comentario:  # Verifica se o usuário existe
                usuario_comentario.quantidadePontos += 1  # Adiciona 1 ponto
                db.session.commit()

            # Enviar notificação para o dono da pergunta, se for um comentário
            if current_user.codigo != pergunta.codUsuario:  # Evita notificar o próprio usuário
                mensagem = f"Nova resposta para sua pergunta: {pergunta.titulo}"
                link_pergunta = url_for('pergunta_route.detalhes_pergunta', pergunta_id=pergunta_id)
                enviar_notificacao(pergunta.codUsuario, mensagem, link_pergunta, pergunta.codigo)

            return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=pergunta_id, sucesso="comentario_realizado"))

    comentarios = comentariosPerguntas.query.filter_by(codPergunta=pergunta_id).all()

    return render_template('detalhes_pergunta.html', pergunta=pergunta, comentarios=comentarios)

@pergunta_route.route('/comentario/<int:comentario_id>/verificar', methods=['POST'])
def verificar_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)
    pergunta = comentario.pergunta_relacionada 

    if current_user.codigo != pergunta.codUsuario:
        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=pergunta.codigo))

    # Impede que comentários denunciados sejam verificados como a melhor resposta
    if comentario.denuncias and len(comentario.denuncias) > 0:
        return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=pergunta.codigo, sucesso="comentario_verificado_denunciado"))

    # Redefine todos os comentários da pergunta para não serem a melhor resposta
    for c in pergunta.comentarios:
        c.melhor_resposta = False

    # Define o comentário atual como a melhor resposta
    comentario.melhor_resposta = True
    db.session.commit()

    return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=pergunta.codigo, sucesso="comentario_verificado"))

@pergunta_route.route('/comentario/<int:comentario_id>/excluir', methods=['POST'])
@login_required
def excluir_comentario_pergunta(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)

    # Caso o comentario da pergunta não seja associada ao usuário, o comentario não poderá ser excluído
    if comentario.codUsuario != current_user.codigo:
        return redirect(url_for('home.homePergunta'))

    try:
        # Excluir o comentário
        db.session.delete(comentario)
        db.session.commit()

        # Diminuir 1 ponto do usuário que excluiu o comentário
        usuario_comentario = Usuario.query.get(comentario.codUsuario)  # Usuário que fez o comentário
        if usuario_comentario:  # Verifica se o usuário existe
            usuario_comentario.quantidadePontos -= 1  # Subtrai 1 ponto
            db.session.commit()

    except IntegrityError:
        # Caso tenha um erro, volta novamente
        db.session.rollback()
    
    return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta, sucesso="comentario_excluido"))

@pergunta_route.route('/comentario/<int:comentario_id>/curtir', methods=['POST'])
@login_required
def like_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)

    # Verifica se o usuário já curtiu o comentário
    curtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codComentarioPergunta=comentario_id,  # Como é um comentário de pergunta
        tipo='like',
        origem='comentario_pergunta'  # Definindo que a origem é comentário de pergunta
    ).first()

    # Verifica se o usuário já deu deslike no comentário
    descurtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codComentarioPergunta=comentario_id,  # Como é um comentário de pergunta
        tipo='deslike',
        origem='comentario_pergunta'  # Definindo que a origem é comentário de pergunta
    ).first()

    if curtida_existente:
        # Se o usuário já deu like, retira o like e não faz nada
        db.session.delete(curtida_existente)
        comentario.quantidadeCurtidas -= 1
        db.session.commit()

        # Decrementa pontos ao dono do comentário
        dono_comentario = Usuario.query.get(comentario.codUsuario)
        dono_comentario.quantidadePontos -= 1  # Ajuste conforme a lógica de pontos
        db.session.commit()

    if descurtida_existente:
        # Se o usuário já deu deslike, retira o deslike e adiciona o like
        db.session.delete(descurtida_existente)  # Exclui o deslike
        comentario.quantidadeCurtidas += 1  # Incrementa a quantidade de curtidas
        db.session.commit()

        # Incrementa pontos ao dono do comentário
        dono_comentario = Usuario.query.get(comentario.codUsuario)
        dono_comentario.quantidadePontos += 1  # Ajuste conforme a lógica de pontos
        db.session.commit()

    # Adiciona uma nova curtida
    nova_curtida = Likes_deslikes(
        codComentarioPergunta=comentario_id,  # Associando ao comentário de pergunta
        codUsuario=current_user.codigo,
        tipo='like',
        origem='comentario_pergunta'  # Definindo a origem como comentário de pergunta
    )
    db.session.add(nova_curtida)

    # Incrementa a quantidade de curtidas no comentário
    comentario.quantidadeCurtidas += 1
    db.session.commit()

    # Incrementa pontos ao dono do comentário
    dono_comentario = Usuario.query.get(comentario.codUsuario)
    dono_comentario.quantidadePontos += 1 
    db.session.commit()

    return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta, sucesso="like_realizado"))

@pergunta_route.route('/comentario/<int:comentario_id>/descurtir', methods=['POST'])
@login_required
def deslike_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)

    # Verifica se o usuário já deu deslike no comentário
    descurtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codComentarioPergunta=comentario_id,  # Como é um comentário de pergunta
        tipo='deslike',
        origem='comentario_pergunta'  # Definindo que a origem é comentário de pergunta
    ).first()

    # Verifica se o usuário já deu like no comentário
    curtida_existente = Likes_deslikes.query.filter_by(
        codUsuario=current_user.codigo,
        codComentarioPergunta=comentario_id,  # Como é um comentário de pergunta
        tipo='like',
        origem='comentario_pergunta'  # Definindo que a origem é comentário de pergunta
    ).first()

    if descurtida_existente:
        # Se o usuário já deu deslike, retira o deslike e não faz nada
        db.session.delete(descurtida_existente)
        comentario.quantidadeCurtidas += 1  # Incrementa a quantidade de curtidas
        db.session.commit()

        # Incrementa pontos ao dono do comentário
        dono_comentario = Usuario.query.get(comentario.codUsuario)
        dono_comentario.quantidadePontos += 1  # Ajuste conforme a lógica de pontos
        db.session.commit()

    if curtida_existente:
        # Se o usuário já deu like, retira o like e adiciona o deslike
        db.session.delete(curtida_existente)  # Exclui o like
        comentario.quantidadeCurtidas -= 1  # Decrementa a quantidade de curtidas
        db.session.commit()

        # Decrementa pontos ao dono do comentário (se necessário)
        dono_comentario = Usuario.query.get(comentario.codUsuario)
        dono_comentario.quantidadePontos -= 1  # Ajuste conforme a lógica de pontos
        db.session.commit()

    # Adiciona uma nova descurtida
    nova_descurtida = Likes_deslikes(
        codComentarioPergunta=comentario_id,  # Associando ao comentário de pergunta
        codUsuario=current_user.codigo,
        tipo='deslike',
        origem='comentario_pergunta'  # Definindo a origem como comentário de pergunta
    )
    db.session.add(nova_descurtida)

    # Decrementa a quantidade de curtidas no comentário
    comentario.quantidadeCurtidas -= 1
    db.session.commit()

    # Decrementa pontos ao dono do comentário (se necessário)
    dono_comentario = Usuario.query.get(comentario.codUsuario)
    dono_comentario.quantidadePontos -= 1  # Ajuste conforme a lógica de pontos
    db.session.commit()

    return redirect(url_for('pergunta_route.detalhes_pergunta', pergunta_id=comentario.codPergunta, sucesso="deslike_realizado"))

# Rota para a barra de pesquisa
@pergunta_route.route('/pesquisar_pergunta', methods=['POST'])
def pergunta_pesquisar():
    pesquisa = request.form.get('pesquisar')

    if pesquisa:
        # Busca as perguntas cujo título ou descrição contenham o termo pesquisado no banco de dados 
        perguntas_encontradas = Pergunta.query.filter(
            (Pergunta.titulo.ilike(f'%{pesquisa}%')) | 
            (Pergunta.descricao.ilike(f'%{pesquisa}'))
        ).all()

        return render_template('homePergunta.html', perguntas=perguntas_encontradas, pesquisa=pesquisa)

    # Se a pesquisa estiver vazia, redireciona para a página inicial
    return redirect(url_for('home.homePergunta'))

# Rota para aparecer as etiquetas no banco de dados ao clicar no input
@pergunta_route.route('/etiquetas_iniciais')
def etiquetas_iniciais():
    # Pega as cinco primeiras etiquetas do banco de dados
    etiquetas = Etiqueta.query.limit(5).all()
    etiquetas_json = [{'codigo': etiqueta.codigo, 'nome': etiqueta.nome} for etiqueta in etiquetas]
    return jsonify(etiquetas_json)

# Rota para pegar as etiquetas relacionadas de acordo com a pesquisa
@pergunta_route.route('/etiquetas_relacionadas')
def etiquetas_relacionadas():
    termo = request.args.get('termo', '')
    
    if termo:
        etiquetas = Etiqueta.query.filter(Etiqueta.nome.ilike(f'%{termo}%')).limit(5).all()
    else:
        etiquetas = []

    etiquetas_json = [{'codigo': etiqueta.codigo, 'nome': etiqueta.nome} for etiqueta in etiquetas]
    return jsonify(etiquetas_json)