from flask import Blueprint, render_template, request, jsonify
import openai
import os

ia_route = Blueprint('ia', __name__)

openai.api_key = 'sk-svcacct-KNCExInW1Ks2qEMqUCVoITq4IA2iPgRkwnVcKMHMp3AvY70tA_uEhdR-S5iYJA8T3BlbkFJIVIfz1Y1LhYl-PRYF8-I-vrqNuB0MLiXShOTisY2s9wHRhkQG4_C2MibeDQE8cAA'

@ia_route.route('/ia', methods=['GET', 'POST'])
def pagina_ia():
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            pergunta = request.json.get('pergunta')
            if pergunta:
                resposta = gerar_resposta_ia(pergunta)
                return jsonify({'resposta': resposta})
        else:
            return jsonify({"error": "Unsupported Media Type"}), 415

    return render_template('ia.html')

def gerar_resposta_ia(pergunta_texto):
    try:
        prompt = "Você é um assistente de IA especializado em responder perguntas de programação. " \
                 "Responda de forma clara e técnica. Pergunta: " + pergunta_texto

        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=1000
        )

        return response.choices[0].text.strip()

    except Exception as e:
        print(f"Erro ao chamar a API OpenAI: {e}")
        return "Erro ao gerar resposta da IA."
