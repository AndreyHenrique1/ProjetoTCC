from flask import Flask, request, jsonify, render_template, Blueprint
import firebase_admin
from firebase_admin import credentials, db

home_route = Blueprint('home', __name__, template_folder='../../front-end/templates')

"""# Inicialize o Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://projeto-tcc-255b4-default-rtdb.firebaseio.com/'
})

# Referência para o banco de dados
ref = db.reference('/')"""

@home_route.route('/')
def home():
    return render_template("home.html")

"""@home_route.route('/perguntas', methods=['POST'])
def criar_pergunta():
    dados = request.json
    nova_pergunta_ref = ref.child('perguntas').push(dados)
    return jsonify({"id": nova_pergunta_ref.key}), 201

@home_route.route('/perguntas', methods=['GET'])
def ler_perguntas():
    perguntas = ref.child('perguntas').get()
    return jsonify(perguntas), 200

@home_route.route('/perguntas/<id>', methods=['GET'])
def ler_pergunta(id):
    pergunta = ref.child('perguntas').child(id).get()
    if pergunta:
        return jsonify(pergunta), 200
    else:
        return jsonify({"error": "Pergunta não encontrada"}), 404

@home_route.route('/perguntas/<id>', methods=['PUT'])
def atualizar_pergunta(id):
    dados = request.json
    pergunta_ref = ref.child('perguntas').child(id)
    
    if pergunta_ref.get():
        pergunta_ref.update(dados)
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Pergunta não encontrada"}), 404

@home_route.route('/perguntas/<id>', methods=['DELETE'])
def deletar_pergunta(id):
    pergunta_ref = ref.child('perguntas').child(id) 
    if pergunta_ref.get():
        pergunta_ref.delete()
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Pergunta não encontrada"}), 404"""