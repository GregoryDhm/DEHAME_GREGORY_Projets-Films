from flask import Flask, render_template
from cgitb import html
from http import HTTPStatus
import sql

app = Flask(__name__)

from blueprints.films import films_app
app.register_blueprint(films_app)

#Route pour la page d'accueil
@app.route('/')
def index():
    return render_template("index.jinja")

#Route pour la page d'erreur 404
@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404

#Route pour initialiser la base de données
@app.before_first_request
def initialize():
    sql.init()

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()