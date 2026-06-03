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

def connect(save: cg.ConfigParser, dbh: db.DBHandler, inter: ui.UI) -> bool:
    if not is_logged():
        (email, pwd) = inter.connexionWindow()
        if inter.action_id == 0:
            signed = is_signed(dbh, email, pwd)
            if signed:
                user = dbh.c_query("SELECT * FROM users WHERE email = %s", (email), True)
                print(user)
                create_log(save, user[0][3], user[0][4], user[0][0], user[0][1], user[0][2], user[0][5])
                return True
            else:
                inter.print_message("L'adresse mail ou le mot de passe est incorrect !", "Connexion Error")
                return False
        elif inter.action_id == 1:
            inter.resetID()
            (fn, ln, em, pwdd, ville) = inter.creationWindow()
            if inter.action_id == -1:
                return False
            elif inter.action_id == None:
                exit()
            emails = dbh.s_query("SELECT email from users", True)
            emails = [em[0] for em in emails]
            while fn == "" or ln == "" or len(pwdd) < 8 or pwd.count(" ") > 0 or em in emails:
                inter.print_message(
                    "Certaines des informations fournies sont erronées. Liste des raisons potentielles :\n" \
                    "- Le nom ou le prénom est vide\n" \
                    "- La longueur du mot de passe est inférieure à 8\n" \
                    "- Le mot de passe contient des espaces\n" \
                    "- L'adresse mail fournie est déjà enregistrée sur un compte",
                    "Account creation error"
                )
                (fn, ln, em, pwdd, ville) = inter.creationWindow()
                if inter.action_id == -1:
                    return False
                elif inter.action_id == None:
                    exit()
            dbh.c_query("INSERT INTO users (firstname, lastname, email, password_hash, city) VALUES (%s, %s, %s, %s, %s)", (fn, ln, em, pwdd, ville), False)
            idd = dbh.c_query("SELECT id FROM users WHERE email = %s", (em), True)[0][0]
            create_log(save, em, pwdd, idd, fn, ln, ville)
            return True
        else:
            exit()
    else:
        return True

def run(save: cg.ConfigParser, dbh: db.DBHandler, inter: ui.UI):
    c = connect(save, dbh, inter)
    while not c:
        c = connect(save, dbh, inter)
    save.read("log.ini")

    while True:
        user = save.items(section = "id")[0][1]
        inter.accueilWindow(user)
        if inter.action_id == 0:
            inter.resetID()
            inter.profilWindow(user)
            if inter.action_id == -1:
                pass
            elif inter.action_id == 0:
                inter.creationAnnonceWindow(user)
            else:
                exit()
            inter.resetID()
        elif inter.action_id == 1:
            inter.resetID()
            inter.listeAnnoncesWindow(user)
            if inter.action_id == -1:
                pass
            elif inter.action_id != None:
                annonce_id = inter.action_id
                inter.resetID()
                inter.detailAnnonceWindow(annonce_id)
                if inter.action_id == -1:
                    pass
            else:
                exit()
            inter.resetID()
        else:
            exit()


run(save, dbh, inter)