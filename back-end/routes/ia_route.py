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
    prompt = (
        "Você é um assistente de IA especializado em responder perguntas de programação. "
        "Responda de forma clara e técnica. Pergunta: " + pergunta_texto
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente de IA especializado em programação."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()
