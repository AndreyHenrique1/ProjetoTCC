from flask import render_template, Blueprint

sobreNos_route = Blueprint('sobreNos', __name__, template_folder='../../front-end/templates')

# Rota de explicação de como funciona o DevSolve
@sobreNos_route.route('/ajuda')
def sobre_nos():
    return render_template('sobre_nos.html')