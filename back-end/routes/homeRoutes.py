from flask import Flask, request, jsonify, render_template, Blueprint
import firebase_admin
from firebase_admin import credentials, db
from database.db import db
from models.pergunta import Pergunta

home_route = Blueprint('home', __name__, template_folder='../../front-end/templates')

@home_route.route('/')
def home():
    return render_template("home.html")

