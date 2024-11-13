from flask import Blueprint, render_template, request, jsonify
import openai

ia_route = Blueprint('ia', __name__)
openai.api_key = 'sk-svcacct-KNCExInW1Ks2qEMqUCVoITq4IA2iPgRkwnVcKMHMp3AvY70tA_uEhdR-S5iYJA8T3BlbkFJIVIfz1Y1LhYl-PRYF8-I-vrqNuB0MLiXShOTisY2s9wHRhkQG4_C2MibeDQE8cAA'

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
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente de IA especializado em programação."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response['choices'][0]['message']['content'].strip()
