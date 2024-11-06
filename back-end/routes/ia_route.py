from flask import Blueprint, render_template, request, jsonify
import openai

ia_route = Blueprint('ia', __name__)
openai.api_key = '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'

@ia_route.route('/ia', methods=['GET', 'POST'])
def pagina_ia():
    if request.method == 'POST':
        pergunta = request.json.get('pergunta')
        if pergunta:
            resposta = gerar_resposta_ia(pergunta)
            return jsonify({'resposta': resposta})
    return render_template('ia.html')

def gerar_resposta_ia(pergunta_texto):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=pergunta_texto,
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()
