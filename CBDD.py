import mysql.connector

class CBDD():
    def __init__(self):
        return
        #Informations de connexion de la base de données


    def WriteBDD(self, data):
        conn = mysql.connector.connect(host="localhost",user="root",password="", database="acquisition")
        cursor = conn.cursor()

        #Création de la table mesures si elle n'existe pas déjà
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mesures (
            id int(5) NOT NULL AUTO_INCREMENT,
            Temps FLOAT DEFAULT NULL,
            Valeurs FLOAT DEFAULT NULL,
            Capteur_id INTEGER DEFAULT NULL,
            PRIMARY KEY(id)
        );
        """)

        #Récupération des informations envoyées lors de l'appelle de la fonction
        temps = data[0]
        valeur = data[1]
        capteur_id = data[2]

        #Tableau contenant les données à écrire dans la base de données
        tabData = (temps, valeur, capteur_id)

        #Ecriture dans la table mesures
        cursor.execute("""INSERT INTO mesures (Temps, Valeurs, Capteur_id) VALUES(%s, %s, %s)""", tabData)

        #Fermeture de la connexion
        conn.close()


#donnees=(0.0, -0.0006699347938052824, 1)
##print(donnees)
#bdd = CBDD()
#bdd.WriteBDD(donnees)
