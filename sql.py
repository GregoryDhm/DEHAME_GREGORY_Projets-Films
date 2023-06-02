import sqlite3
import os

bd = 'base_de_donnees.db'
cheminAffiche = 'static/affiches/'

#Insertion d'un film dans la base de données
def insert(data):
    conn = sqlite3.connect(bd)
    c = conn.cursor()
    #print(data)
    # Insertion des données
    c.execute("INSERT INTO films (id, titre, description_film, annee_sortie, realisateur, acteur1, acteur2, affiche) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data['id'], data['nomFilm'], data['Description'], data['annee'], data['realisateur'], data['acteur1'], data['acteur2'], data['affiche']))
    # Validation de la transaction et fermeture de la connexion
    conn.commit()
    conn.close()

#Récupération de tous les films
def get_films(trie):
    # Connexion à la base de données
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    # Exécution de la requête SQL
    cursor.execute(f"SELECT titre, description_film, annee_sortie, realisateur, acteur1, acteur2, affiche, id FROM films ORDER BY {trie}")
    # Récupération des résultats
    result = cursor.fetchall()
    # Fermeture de la connexion à la base de données
    conn.close()
    # Retourne les résultats
    return result

#Récupération d'un film
def get_film(id):
    # Connexion à la base de données
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    # Exécution de la requête SQL
    cursor.execute("SELECT titre, description_film, annee_sortie, realisateur, acteur1, acteur2, affiche, id FROM films WHERE id = ?", (id,))
    # Récupération des résultats
    result = cursor.fetchone()
    # Fermeture de la connexion à la base de données
    conn.close()
    # Retourne les résultats
    return result

#Update d'un film
def edit(id, data):
    conn = sqlite3.connect(bd)
    c = conn.cursor()
    #print(data)
    # Insertion des données
    c.execute("UPDATE films SET titre = ?, description_film = ?, annee_sortie = ?, realisateur = ?, acteur1 = ?, acteur2 = ? WHERE id = ?", (data['nomFilm'], data['Description'], data['annee'], data['realisateur'], data['acteur1'], data['acteur2'], id))
    # Validation de la transaction et fermeture de la connexion
    conn.commit()
    conn.close()

#Suppression d'un film
def delete_film(id):
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    cursor.execute("SELECT affiche FROM films WHERE id = ?", (id,))
    afficheName = cursor.fetchone()[0]
    if afficheName is not None and afficheName != '':
        os.remove(cheminAffiche + afficheName)
    cursor.execute("DELETE FROM films WHERE id = ?", (id,))  
    conn.commit()
    conn.close()

#Initialisation de la base de données
def init():
    # Ouverture d'une connexion à la base de données
    conn = sqlite3.connect(bd)
    # Création d'une table dans la base de données
    conn.execute('CREATE TABLE IF NOT EXISTS films (id INTEGER PRIMARY KEY, titre VARCHAR(100) NOT NULL,description_film TEXT,annee_sortie DATE,realisateur VARCHAR(50), acteur1 VARCHAR(50), acteur2 VARCHAR(50), affiche VARCHAR(50))')
    # Fermeture de la connexion à la base de données
    conn.close()
    