from flask import request, render_template, Blueprint, redirect, url_for

ajuda_route = Blueprint('ajuda', __name__, template_folder='../../front-end/templates')

# Rota de ajuda do site (Explicação de como funciona o DevSolve)
@ajuda_route.route('/ajuda')
def ajuda():
    return render_template('ajuda.html')