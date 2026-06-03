import UI as ui
import DBHandling as db
import configparser as cg
import os

save = cg.ConfigParser()
dbh = db.DBHandler()
inter = ui.UI(dbh)

def is_signed(dbh: db.DBHandler, email, pwd):
    res = dbh.c_query("SELECT * FROM users WHERE email = %s AND password_hash = %s", (email, pwd), True)
    return res != ()

def is_logged():
    return os.path.isfile("log.ini")

def create_log(save: cg.ConfigParser, email, pwd, id, firstname, lastname, city):
    save.add_section('email')
    save.add_section('pwd')
    save.add_section('id')
    save.add_section('names')
    save.add_section('city')
    save.set('email', 'e', email)
    save.set('pwd', 'p', pwd)
    save.set('id', 'i', str(id))
    save.set('names', 'firstname', firstname)
    save.set('names', 'lastname', lastname)
    save.set('city', 'c', city)
    with open ('log.ini', "w") as file:
        save.write(file)

def connect(save: cg.ConfigParser, dbh: db.DBHandler, inter: ui.UI):
    if not is_logged():
        (email, pwd) = inter.connexionWindow()
        if inter.action_id == 0:
            signed = is_signed(dbh, email, pwd)
            if signed:
                print("Connexion successfull")
            else:
                inter.print_message("L'adresse mail ou le mot de passe est incorrect !", "Connexion Error")
                exit()
        elif inter.action_id == 1:
            inter.resetID()
            inter.creationWindow()
            inter.resetID()
        else:
            exit()

def run(save: cg.ConfigParser, dbh: db.DBHandler, inter: ui.UI):
    connect(save, dbh, inter)
    save.read("log.ini")

    while True:
        inter.accueilWindow()
        if inter.action_id == 0:
            inter.profilWindow(save.items(section = "id")[1])
            if inter.action_id == -1:
                pass
        elif inter.action_id == 1:
            inter.listeAnnoncesWindow()
            if inter.action_id == -1:
                pass
        else:
            exit()


run(save, dbh, inter)