from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database.db import db
from models.pergunta import Pergunta
from models.comentariosPerguntas import comentariosPerguntas 
from models.categoria import Categoria
from models.Etiqueta import Etiqueta
from models.curtidasComentarios import CurtidasComentarios  
from models.usuario import Usuario
from models.perguntasEtiquetas import PerguntasEtiquetas
from models.notificacao import enviar_notificacao
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

pergunta_route = Blueprint('pergunta_route', __name__)

@pergunta_route.route('/etiquetas_populares', methods=['GET'])
def etiquetas_populares():
    search = request.args.get('search', '')  # Obtém o parâmetro de busca
    etiquetas = Etiqueta.query.filter(Etiqueta.nome.ilike(f'{search}%')).order_by(Etiqueta.popularidade.desc()).limit(10).all()
    return jsonify([etiqueta.nome for etiqueta in etiquetas])


@pergunta_route.route('/etiquetas/<termo>')
def etiquetas(termo):
    etiquetas = Etiqueta.query.filter(Etiqueta.nome.ilike(f'%{termo}%')).all()
    return jsonify([etiqueta.nome for etiqueta in etiquetas])

# Rota para criar as perguntas e etiquetas recebidas
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

        #Adiciona a pergunta no banco de dados
        nova_pergunta = Pergunta(titulo=titulo, descricao=descricao, codCategoria=codCategoria, codUsuario=codUsuario)
        db.session.add(nova_pergunta)
        db.session.commit()

        # Pega cada etiqueta separadamente
        for nome_etiqueta in etiquetas_lista:
            etiqueta_objeto = Etiqueta.query.filter_by(nome=nome_etiqueta).first()

            # Verifica se a etiqueta já existe
            if etiqueta_objeto:
                #Caso exista a etiqueta aumenta +1 na popularidade
                etiqueta_objeto.popularidade += 1

            # Caso a etiqueta não esteja no banco de dados 
            else:
                # Cria uma nova etiqueta
                etiqueta_objeto = Etiqueta(nome=nome_etiqueta, popularidade=1)
                db.session.add(etiqueta_objeto)
                db.session.commit() 

            # Associa a etiqueta à pergunta
            nova_pergunta_etiqueta = PerguntasEtiquetas(codPergunta=nova_pergunta.codigo, codEtiqueta=etiqueta_objeto.codigo)
            db.session.add(nova_pergunta_etiqueta)

        # Commit final para associar etiquetas e pergunta
        db.session.commit()  

        return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=nova_pergunta.codigo))

    etiquetas = Etiqueta.query.all()
    categorias = Categoria.query.all()
    return render_template('perguntar.html', categorias=categorias, etiquetas=etiquetas)

# Rota para editar perguntas
@pergunta_route.route('/pergunta/<int:pergunta_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    
    if pergunta.codUsuario != current_user.codigo:
        flash("Você não tem permissão para editar essa pergunta.")
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        pergunta.titulo = request.form['titulo']
        pergunta.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=pergunta_id))

    return render_template('editar_pergunta.html', pergunta=pergunta)

# Rota para excluir pergunta
@pergunta_route.route('/pergunta/<int:pergunta_id>/excluir', methods=['POST'])
@login_required
def excluir_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    
    if pergunta.codUsuario != current_user.codigo:
        flash("Você não tem permissão para excluir essa pergunta.")
        return redirect(url_for('home.home'))

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

    # Excluir todos os comentários relacionados à pergunta
    comentariosPerguntas.query.filter_by(codPergunta=pergunta.codigo).delete()

    # Excluir a pergunta
    db.session.delete(pergunta)
    db.session.commit()
    
    return redirect(url_for('home.home'))

# Detalhes e comentários da pergunta
@pergunta_route.route('/pergunta/<int:pergunta_id>', methods=['GET', 'POST'])
def pergunta_detalhe(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)

    if request.method == 'POST':
        conteudo_comentario = request.form.get('conteudo_comentario')

        if conteudo_comentario and current_user.is_authenticated:
        # Quando alguém responde a uma pergunta
            novo_comentario = comentariosPerguntas(
            comentario=conteudo_comentario, codPergunta=pergunta_id, codUsuario=current_user.codigo
            )
            db.session.add(novo_comentario)
            db.session.commit()

            # Enviar notificação para o dono da pergunta
            if current_user.codigo != pergunta.codUsuario:  # Evitar notificar o próprio usuário
                mensagem = f"Você recebeu uma nova resposta para sua pergunta: {pergunta.titulo}"
                link_pergunta = url_for('pergunta_route.pergunta_detalhe', pergunta_id=pergunta_id)
                enviar_notificacao(pergunta.codUsuario, mensagem, link_pergunta, pergunta.codigo)


            return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=pergunta_id))

    comentarios = comentariosPerguntas.query.filter_by(codPergunta=pergunta_id).all()

    return render_template('pergunta_detalhe.html', pergunta=pergunta, comentarios=comentarios)

# Rota para excluir comentário
@pergunta_route.route('/comentario/<int:comentario_id>/excluir', methods=['POST'])
@login_required
def excluir_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)

    if comentario.codUsuario != current_user.codigo:
        flash("Você não tem permissão para excluir esse comentário.")
        return redirect(url_for('home.home'))

    try:
        db.session.delete(comentario)
        db.session.commit()
        flash("Comentário excluído com sucesso.")
    except IntegrityError:
        db.session.rollback()
        flash("Ocorreu um erro ao excluir o comentário.")
    
    return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=comentario.codPergunta))

# Rota para curtir um comentário
@pergunta_route.route('/comentario/<int:comentario_id>/curtir', methods=['POST'])
@login_required
def curtir_comentario(comentario_id):
    comentario = comentariosPerguntas.query.get_or_404(comentario_id)

    # Verifica se o usuário já curtiu o comentário
    curtida_existente = CurtidasComentarios.query.filter_by(codUsuario=current_user.codigo, codComentario=comentario_id).first()
    if curtida_existente:
        flash('Você já curtiu este comentário.')
        return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=comentario.codPergunta))

    # Adiciona uma nova curtida
    nova_curtida = CurtidasComentarios(codComentario=comentario_id, codUsuario=current_user.codigo)
    db.session.add(nova_curtida)

    # Incrementa a quantidade de curtidas no comentário
    comentario.quantidadeCurtidas += 1
    db.session.commit()

    # Incrementa pontos ao dono do comentário
    dono_comentario = Usuario.query.get(comentario.codUsuario)
    dono_comentario.quantidadePontos += 1  # Adiciona 1 ponto
    db.session.commit()

    flash('Comentário curtido com sucesso!')
    return redirect(url_for('pergunta_route.pergunta_detalhe', pergunta_id=comentario.codPergunta))

# Rota para a barra de pesquisa
@pergunta_route.route('/pesquisar', methods=['POST'])
def pesquisar():
    pesquisa = request.form.get('pesquisar')

    if pesquisa:
        # Busca as perguntas cujo título ou descrição que contenham no banco de dados 
        perguntas_encontradas = Pergunta.query.filter(
            (Pergunta.titulo.ilike(f'%{pesquisa}%')) | 
            (Pergunta.descricao.ilike(f'%{pesquisa}%'))
        ).all()

        # Renderiza a página principal com as perguntas filtradas
        return render_template('home.html', perguntas=perguntas_encontradas, pesquisa=pesquisa)

    # Se a pesquisa estiver vazia, redireciona para a página inicial
    flash('Por favor, insira um termo para pesquisa.')
    return redirect(url_for('home.home'))

