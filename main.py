import UI as ui
import DBHandling as db

# 1. Initialiser la connexion à la base de données
database = db.DBHandler()
database.connect_DB("root") 

# 2. Passer la base de données à l'interface
app = ui.UI(database)

# 3. Boucle principale de navigation (Le Routeur)
app.action_id = 2 # On force le démarrage sur l'accueil pour tester

while True:
    if app.action_id is None:
        # Fermeture de la fenêtre par la croix rouge
        print("Fermeture de l'application.")
        break
        
    elif app.action_id == 2:
        # Lancement de la fenêtre Accueil
        app.accueilWindow()
        
    elif app.action_id == 3:
        # ACTIVATION : On lance la vraie méthode de la liste des annonces
        print("Ouverture du catalogue...")
        app.listeAnnoncesWindow()
        
    elif app.action_id == 7:
        # ACTIVATION : On lance la vraie méthode du profil utilisateur
        print("Ouverture du profil utilisateur...")
        app.profilWindow()