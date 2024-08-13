from flask import Flask
from configuration import configure_all

#Inicializar o flask
app = Flask(__name__)

configure_all(app)

#Execução
app.run(debug=True)

