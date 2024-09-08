from flask import Flask
from configuration import configure_all

#Inicializar o flask
app = Flask(__name__, static_folder='../front-end/static')

configure_all(app)

#Execução
app.run(debug=True)

