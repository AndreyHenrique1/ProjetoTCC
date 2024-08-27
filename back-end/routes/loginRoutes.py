from flask import Flask, render_template, Blueprint

login_route = Blueprint('login', __name__, template_folder='../../front-end/templates', url_prefix='/Login')

@login_route.route('/', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


