from flask import Flask, Blueprint, redirect, request, url_for, render_template, make_response, send_file
from cgitb import html
from http import HTTPStatus
import sql,helper
from datetime import datetime

films_app = Blueprint('films_app',__name__)

#Route pour la page d'accueil des films
@films_app.route('/films', methods=['GET'])
def getFilms():
    valid_trie = ['titre', 'annee_sortie']
    sort = request.args.get('sort')
    order = request.args.get('order')
    if sort is None or sort not in valid_trie:
        sort = 'titre'
    order = 'asc' if order != 'desc' else 'desc'
    data=sql.get_films(sort + " " + order)
    for (i, row) in enumerate(data):
        data[i] = list(row)
        data[i][6] = helper.faceDetect(data[i][6]) #ajout de la detection de visage sur toutes les images.
    return render_template("films.jinja", data=data, cheminAffiche=sql.cheminAffiche, sort=sort, order=order)

#Route création d'un film
@films_app.route('/film/add', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # Traitement des données envoyées en POST
        nomFilm = request.form['nomFilm']
        Description = request.form['description']
        annee = request.form['annee']
        acteur1 = request.form['acteur1']
        acteur2 = request.form['acteur2']
        realisateur = request.form['realisateur']
        affiche = request.files['image']

        # génération d'un id unique tel que AAAAMMJJHHMMSSmmm
        id = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

        afficheName = ''

        if affiche:
            afficheName = id + '.' + affiche.filename.rsplit('.', 1)[1].lower()
            affiche.save(sql.cheminAffiche + afficheName)

        data = {
            'id' : id,
            'nomFilm': nomFilm, 
            'Description': Description,
            'annee': annee, 
            'acteur1':acteur1,
            'acteur2':acteur2,
            'realisateur':realisateur,
            'affiche' : afficheName
            }
        sql.insert(data)

        return redirect(url_for('index'))
    else:
        return render_template("addFilm.jinja", requestMethod=request.method)
    
#route pour voir le détail d'un film
@films_app.route('/film/<id>')
def getFilm(id):
    data = sql.get_film(id)
    #return render_template("film.jinja", data=data, affiche= "/" + sql.cheminAffiche + data[6], id=id)
    #print(sql.cheminAffiche + data[6])
    return render_template("film.jinja", data=data, image_base64=helper.faceDetect(data[6]), id=id)

#route edit film
@films_app.route('/film/edit/<id>', methods=['GET', 'POST'])
def editFilm(id):
    if request.method == 'GET':
        data = sql.get_film(id)
        return render_template("editFilm.jinja", data=data, id=id, affiche= "/" + sql.cheminAffiche + data[6])
    if request.method == 'POST':
        # Traitement des données envoyées en POST
        nomFilm = request.form['nomFilm']
        Description = request.form['description']
        annee = request.form['annee']
        acteur1 = request.form['acteur1']
        acteur2 = request.form['acteur2']
        realisateur = request.form['realisateur']
        #affiche = request.files['image']
            
        afficheName = ''

        #if affiche:
        #    afficheName = id + '.' + affiche.filename.rsplit('.', 1)[1].lower()
        #    affiche.save(sql.cheminAffiche + afficheName)

        data = {
            'nomFilm': nomFilm, 
            'Description': Description,
            'annee': annee, 
            'acteur1':acteur1,
            'acteur2':acteur2,
            'realisateur':realisateur
            #'affiche' : afficheName
        }
        sql.edit(id, data)
        return redirect(url_for('films_app.getFilm', id=id)) 

#route delete_film
@films_app.route('/film/delete/<id>', methods=['GET'])
def deleteFilm(id):
    sql.delete_film(id)
    return redirect(url_for('getFilms'))