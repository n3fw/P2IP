import tkinter as tk
from tkinter import messagebox
import ctypes as ct
import os

class UI():
    def __init__(self, db_handler):
        self.root = None
        self.size = "600x400"
        self.color = "000000"
        self.action_id = None
        self.icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ressources", "main_icon.ico")
        self.progress = None
        self.db = db_handler
        self.font = "Arial"
    
    def resetID(self):
        self.action_id = None
    
    def print_message(self, mess: str, wind_title: str):
        ct.windll.user32.MessageBoxW(0, mess, wind_title, 0)
    
    def connexionWindow(self):
        """
        fenêtre pour entrer son mdp et email\n
        possède un bouton connection une fois les infos entrées, le programme s'arrête si elle sont fausses (pas trouvé un moyen de faire plus \n
        user-friendly sans passer une plombe à tout changer)\n
        possède un deuxième bouton de création de compte 
        action_id == 0 -> connection
        action_if == 1 -> creation
        """
        self.root = tk.Tk()
        self.root.geometry("500x350")
        self.root.iconbitmap(self.icon)
        self.root.title("Connection")
        self.root.configure(bg="white")

        def connect():
            self.action_id = 0
            self.root.destroy()
        def create():
            self.action_id = 1
            self.root.destroy()

        tText = tk.Label(self.root, font = (self.font, 20), text = "Connect to your account", bg = "white", fg = "#17E63C")
        tText.place_configure(relx = 0.19, rely = 0.3)

        uText = tk.Label(self.root, font = (self.font, 10), text = "Email address", bg = "white", fg = "black")
        uText.place_configure(relx = 0.25, rely = 0.42)

        pText = tk.Label(self.root, font = (self.font, 10), text = "Password", bg = "white", fg = "black")
        pText.place_configure(relx = 0.25, rely = 0.56)

        iLogo = tk.PhotoImage(file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ressources", "main_icon.png"))
        iLogo = iLogo.subsample(2, 2)
        iLogoLabel = tk.Label(master = self.root, image = iLogo)
        iLogoLabel.pack(anchor = 'n')

        uVar = tk.StringVar()
        uEntry = tk.Entry(self.root, width = 40, textvariable = uVar, bg = "#DBD9D9", fg = "black")
        uEntry.place_configure(relx = 0.255, rely = 0.48)

        pVar = tk.StringVar()
        pEntry = tk.Entry(self.root, width = 40, textvariable = pVar, show="•", bg = "#DBD9D9", fg = "black")
        pEntry.place_configure(relx = 0.255, rely = 0.62)

        CreateButton = tk.Button(self.root, text = "Créer un compte", command=create)
        ConnectButton = tk.Button(self.root, text = "Connection", command=connect)
        CreateButton.place_configure(rely = 0.72, relx = 0.255)
        ConnectButton.place_configure(rely = 0.72, relx = 0.595)

        self.root.mainloop()

        return (uVar.get(), pVar.get())
    
    def creationWindow(self):
        """
        cette fenêtre a juste pour objectif de demander les infos de l'utilisateur à entrer pour la création de compte\n
        les tests sur les infos se font dans le main, après la fin de la fenêtre\n
        retourne un tuple (prenom, nom, email, password, ville)
        action_id == 1 -> retour à la connexion
        action_id == 2 -> création validée
        """
        self.root = tk.Tk()
        self.root.geometry("500x560")
        self.root.iconbitmap(self.icon)
        self.root.title("Créer un compte")
        self.root.configure(bg="white")

        def retour():
            self.action_id = -1
            self.root.destroy()

        def valider():
            prenom = prenomVar.get().strip()
            nom    = nomVar.get().strip()
            email  = emailVar.get().strip()
            pwd    = pwdVar.get().strip()
            pwd2   = pwd2Var.get().strip()
            ville  = villeVar.get().strip()

            if not all([prenom, nom, email, pwd, pwd2]):
                errLabel.config(text="Veuillez remplir tous les champs obligatoires.")
                return
            if pwd != pwd2:
                errLabel.config(text="Les mots de passe ne correspondent pas.")
                return
            if len(pwd) < 4:
                errLabel.config(text="Mot de passe trop court (4 caractères min.).")
                return

            self.action_id = 2
            self.root.destroy()

        # Titre
        tk.Label(self.root, font=(self.font, 18), text="Créer un compte",
                 bg="white", fg="#17E63C").place(relx=0.22, rely=0.02)

        # Prénom
        tk.Label(self.root, font=(self.font, 10), text="Prénom *",
                 bg="white", fg="black").place(relx=0.25, rely=0.10)
        prenomVar = tk.StringVar()
        tk.Entry(self.root, width=40, textvariable=prenomVar,
                 bg="#DBD9D9", fg="black").place(relx=0.255, rely=0.16)

        # Nom
        tk.Label(self.root, font=(self.font, 10), text="Nom *",
                 bg="white", fg="black").place(relx=0.25, rely=0.24)
        nomVar = tk.StringVar()
        tk.Entry(self.root, width=40, textvariable=nomVar,
                 bg="#DBD9D9", fg="black").place(relx=0.255, rely=0.30)

        # Email
        tk.Label(self.root, font=(self.font, 10), text="Adresse email *",
                 bg="white", fg="black").place(relx=0.25, rely=0.38)
        emailVar = tk.StringVar()
        tk.Entry(self.root, width=40, textvariable=emailVar,
                 bg="#DBD9D9", fg="black").place(relx=0.255, rely=0.44)

        # Mot de passe
        tk.Label(self.root, font=(self.font, 10), text="Mot de passe *",
                 bg="white", fg="black").place(relx=0.25, rely=0.52)
        pwdVar = tk.StringVar()
        tk.Entry(self.root, width=40, textvariable=pwdVar, show="•",
                 bg="#DBD9D9", fg="black").place(relx=0.255, rely=0.58)

        # Confirmer mot de passe
        tk.Label(self.root, font=(self.font, 10), text="Confirmer le mot de passe *",
                 bg="white", fg="black").place(relx=0.25, rely=0.66)
        pwd2Var = tk.StringVar()
        tk.Entry(self.root, width=40, textvariable=pwd2Var, show="•",
                 bg="#DBD9D9", fg="black").place(relx=0.255, rely=0.72)

        # Ville (optionnel)
        tk.Label(self.root, font=(self.font, 9), text="Ville (optionnel)",
                 bg="white", fg="gray").place(relx=0.25, rely=0.80)
        villeVar = tk.StringVar()
        tk.Entry(self.root, width=20, textvariable=villeVar,
                 bg="#DBD9D9", fg="black").place(relx=0.255, rely=0.86)

        # Message d'erreur
        errLabel = tk.Label(self.root, font=(self.font, 9), text="",
                            bg="white", fg="red")
        errLabel.place(relx=0.25, rely=0.93)

        # Boutons en bas
        tk.Button(self.root, text="← Retour", command=retour).place(relx=0.255, rely=0.93)
        tk.Button(self.root, text="Créer mon compte", command=valider).place(relx=0.55, rely=0.93)

        self.root.mainloop()

        return (prenomVar.get().strip(), nomVar.get().strip(),
                emailVar.get().strip(), pwdVar.get().strip(),
                villeVar.get().strip())

    def catalogueWindow(self):
        self.root = tk.Tk()
        self.root.geometry(self.size)
        self.root.title("EcoLend - Catalogue des objets")

        def click_deconnexion():
            self.action_id = None
            self.root.quit()
            
        def click_ajouter_objet():
            self.action_id = 2
            self.root.quit()

        tk.Label(self.root, text="Catalogue des objets disponibles", font=("Helvetica", 18)).pack(pady=20)
        objets = ["Perceuse à percussion", "Tente de camping 4 places", "Service à fondue", "Drone DJI"]
        for obj in objets:
            tk.Label(self.root, text=f"📦 {obj}", font=("Helvetica", 12)).pack(anchor="w", padx=50, pady=5)

        tk.Button(self.root, text="Proposer un objet", command=click_ajouter_objet).pack(pady=20)
        tk.Button(self.root, text="Se déconnecter", command=click_deconnexion).pack(pady=10)

        self.root.mainloop()
        self.root.destroy()

    def accueilWindow(self, user_id):
        """
        fenêtre d'acceuil qui affiche les annonces actuelles, sur laquelle est branché le programme après connection / creation de compte
        """
        self.root = tk.Tk()
        self.root.title("P2IP - Accueil & Recherche")
        self.root.geometry(self.size)
        self.root.configure(bg="#F4F6F8")

        cats_db = self.db.s_query("SELECT name FROM categories", ret=True)
        CATEGORIES = ["Toutes"] + [c[0] for c in (cats_db or [])]

        query_annonces = """
            SELECT L.id, L.title, L.description, C.name, U.city 
            FROM listings L
            JOIN categories C ON L.category_id = C.id
            JOIN users U ON L.user_id = U.id
            WHERE L.status = 'active'
            AND U.id != %s
        """
        annonces_db = self.db.c_query(query_annonces, (user_id), ret=True)
        
        self.search_var = tk.StringVar(self.root)
        self.cat_var = tk.StringVar(self.root, value="Toutes")

        def go_to_profil():
            canvas.unbind_all("<MouseWheel>")
            self.action_id = 0
            self.root.quit()
            
        def go_to_liste_annonces():
            canvas.unbind_all("<MouseWheel>")
            self.action_id = 1
            self.root.quit()

        topbar = tk.Frame(self.root, bg="#2D6A4F", padx=16, pady=10)
        topbar.pack(fill="x")

        tk.Label(topbar, text=" P2IP", font=("Helvetica", 18, "bold"), fg="#FFFFFF", bg="#2D6A4F").pack(side="left")

        tk.Button(topbar, text=" Mon profil", bg="#B7E4C7", fg="#2D6A4F", relief="flat",
                  command=go_to_profil).pack(side="right")

        tk.Button(topbar, text="Rechercher (Voir Liste)", bg="#52B788", fg="#FFFFFF", relief="flat",
                  command=go_to_liste_annonces).pack(side="right", padx=10)

        main_container = tk.Frame(self.root, bg="#F4F6F8")
        main_container.pack(fill="both", expand=True, padx=16, pady=12)

        canvas = tk.Canvas(main_container, bg="#F4F6F8", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        body = tk.Frame(canvas, bg="#F4F6F8")
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            # On calcule la taille totale du contenu
            bbox = canvas.bbox("all")
            # On ne scroll QUE si le contenu est plus grand que la zone visible
            if bbox and bbox[3] > canvas.winfo_height():
                canvas.yview_scroll(int(-1(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        tk.Label(body, text="Annonces récentes :", font=("Helvetica", 14, "bold"), bg="#F4F6F8").pack(anchor="w")
        
        if annonces_db:
            for annonce in annonces_db:
                texte = f"{annonce[1]} (Catégorie: {annonce[3]}) - à {annonce[4]}"
                tk.Label(body, text=texte, font=("Helvetica", 11), bg="#FFFFFF", pady=5).pack(fill="x", pady=2)
        else:
            tk.Label(body, text="Aucune annonce en base de données.", bg="#F4F6F8").pack()

        self.root.mainloop()
        self.root.destroy()

    def listeAnnoncesWindow(self, user_id):
        self.root = tk.Tk()
        self.root.title("P2IP – Liste des annonces")
        self.root.geometry(self.size) 
        self.root.configure(bg="#F4F6F8")

        def go_back():
            canvas.unbind_all("<MouseWheel>")
            self.action_id = -1 
            self.root.destroy()

        query = """
            SELECT L.title, C.name, U.city, L.tool_condition, L.description, L.id
            FROM listings L
            JOIN categories C ON L.category_id = C.id
            JOIN users U ON L.user_id = U.id
            WHERE L.status = 'active'
            AND U.id != %s
        """
        annonces = self.db.c_query(query, (user_id), ret=True)

        topbar = tk.Frame(self.root, bg="#2D6A4F", padx=16, pady=10)
        topbar.pack(fill="x")

        tk.Button(topbar, text="← Retour", bg="#2D6A4F", fg="#B7E4C7", relief="flat",
                  font=("Helvetica", 11), cursor="hand2", command=go_back).pack(side="left")
        tk.Label(topbar, text=" P2IP - Catalogue", font=("Helvetica", 16, "bold"),
                 fg="#FFFFFF", bg="#2D6A4F").pack(side="left", padx=16)

        main_container = tk.Frame(self.root, bg="#F4F6F8")
        main_container.pack(fill="both", expand=True, padx=16, pady=12)

        canvas = tk.Canvas(main_container, bg="#F4F6F8", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        container = tk.Frame(canvas, bg="#F4F6F8")

        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            bbox = canvas.bbox("all")
            if bbox and bbox[3] > canvas.winfo_height():
                canvas.yview_scroll(int(-1(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        tk.Label(container, text=f"{len(annonces) if annonces else 0} annonce(s) trouvée(s)", 
                 font=("Helvetica", 11, "bold"), bg="#F4F6F8").pack(anchor="w", pady=(0, 10))

        if annonces:
            for a in annonces:
                def go_to_detail_liste(annonce_id):
                    self.action_id = annonce_id
                    self.root.destroy()

                card = tk.Frame(container, bg="#FFFFFF", relief="flat", bd=1, padx=16, pady=12)
                card.pack(fill="x", pady=6)
                
                head = tk.Frame(card, bg="#FFFFFF")
                head.pack(fill="x")
                tk.Label(head, text=a[0], font=("Helvetica", 14, "bold"), fg="#1B1B2F", bg="#FFFFFF").pack(side="left")
                tk.Label(head, text="Disponible", font=("Helvetica", 8, "bold"), fg="#52B788", bg="#D1FAE5", padx=6, pady=2).pack(side="right")
                
                details_text = f"📍 {a[2]}  •  🏷️ {a[1]}  •  État : {a[3]}"
                tk.Label(card, text=details_text, font=("Helvetica", 9), fg="#6B7280", bg="#FFFFFF").pack(anchor="w", pady=4)
                
                tk.Label(card, text=a[4][:100] + "..." if len(a[4]) > 100 else a[4], 
                         font=("Helvetica", 9), fg="#6B7280", bg="#FFFFFF", wraplength=600, justify="left").pack(anchor="w")
                tk.Button(card, text="Voir le détail →", bg="#2D6A4F", fg="#FFFFFF", relief="flat", font=("Helvetica", 10, "bold"), cursor="hand2", padx=12, pady=4, 
                          command=lambda a_id=a[5]: go_to_detail_liste(a_id)).pack(anchor="e", pady=5)
        else:
            tk.Label(container, text="Aucune annonce ne correspond à votre recherche.", bg="#F4F6F8", fg="#6B7280").pack()

        self.root.mainloop()

    def profilWindow(self, id):
        self.root = tk.Tk()
        self.root.title("P2IP – Mon Profil") 
        self.root.geometry(self.size)
        self.root.configure(bg="#F4F6F8") 

        user_data = self.db.c_query(
            "SELECT firstname, lastname, city FROM Users WHERE id = %s", 
            (id), 
            ret=True
        )
        
        prenom, nom, ville = ("Utilisateur", "Inconnu", "Non renseignée")
        if user_data:
            prenom, nom, ville = user_data[0]

        query_annonces = """
            SELECT L.title, C.name, L.status 
            FROM listings L
            JOIN categories C ON L.category_id = C.id
            WHERE L.user_id = %s
        """
        mes_annonces_db = self.db.c_query(query_annonces, (id), ret=True)

        self.active_tab = tk.StringVar(self.root, value="annonces") 

        def go_back():
            canvas.unbind_all("<MouseWheel>")
            self.action_id = -1
            self.root.quit()
        
        def post_new():
            canvas.unbind_all("<MouseWheel>")
            self.action_id = 0
            self.root.quit()

        def switch_tab(key):
            self.active_tab.set(key)
            for k, btn in tab_btns.items():
                btn.config(bg="#2D6A4F" if k == key else "#FFFFFF",
                           fg="#FFFFFF" if k == key else "#1B1B2F")
            
            for widget in body_frame.winfo_children():
                widget.destroy()
                
            if key == "annonces":
                display_annonces_tab()
            elif key == "locations":
                tk.Label(body_frame, text="Historique de vos emprunts (table Exchange_Offers)...", 
                         font=("Helvetica", 11), bg="#F4F6F8", fg="#6B7280").pack(pady=40)
            elif key == "avis":
                tk.Label(body_frame, text="Aucun avis reçu pour le moment.", 
                         font=("Helvetica", 11), bg="#F4F6F8", fg="#6B7280").pack(pady=40)

        def display_annonces_tab():
            tk.Button(body_frame, text="+ Publier une nouvelle annonce", bg="#52B788", fg="#FFFFFF", 
                      relief="flat", font=("Helvetica", 11, "bold"), cursor="hand2", pady=8,
                      command=post_new).pack(anchor="e", pady=(0, 12))
            
            if mes_annonces_db:
                for a in mes_annonces_db: 
                    card = tk.Frame(body_frame, bg="#FFFFFF", padx=16, pady=10, relief="flat", bd=1)
                    card.pack(fill="x", pady=4)
                    
                    tk.Label(card, text=a[0], font=("Helvetica", 12, "bold"), fg="#1B1B2F", bg="#FFFFFF").pack(anchor="w") 
                    
                    sub = tk.Frame(card, bg="#FFFFFF")
                    sub.pack(anchor="w")
                    tk.Label(sub, text=f"🏷️ {a[1]}", font=("Helvetica", 9), fg="#6B7280", bg="#FFFFFF").pack(side="left")
                    
                    status_color = "#52B788" if a[2] == "disponible" else "#EF4444"
                    tk.Label(sub, text=f"   •   Statut : {a[2]}", font=("Helvetica", 9), fg=status_color, bg="#FFFFFF").pack(side="left")
            else:
                tk.Label(body_frame, text="Vous n'avez aucune annonce en ligne.", font=("Helvetica", 11), bg="#F4F6F8", fg="#6B7280").pack(pady=20)

        topbar = tk.Frame(self.root, bg="#2D6A4F", padx=16, pady=10) 
        topbar.pack(fill="x")
        tk.Button(topbar, text="← Retour", bg="#2D6A4F", fg="#B7E4C7", relief="flat", font=("Helvetica", 11), cursor="hand2", command=go_back).pack(side="left")
        tk.Label(topbar, text=" P2IP  –  Mon Profil", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#2D6A4F").pack(side="left", padx=16) 

        header = tk.Frame(self.root, bg="#FFFFFF", padx=24, pady=20, relief="flat", bd=1)
        header.pack(fill="x")

        info_frame = tk.Frame(header, bg="#FFFFFF")
        info_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(info_frame, text=f"{prenom} {nom}", font=("Helvetica", 15, "bold"), fg="#1B1B2F", bg="#FFFFFF").pack(anchor="w") 
        tk.Label(info_frame, text=f"📍 {ville}", font=("Helvetica", 10), fg="#6B7280", bg="#FFFFFF").pack(anchor="w") 

        tabs = tk.Frame(self.root, bg="#FFFFFF")
        tabs.pack(fill="x")
        
        tab_btns = {}
        for label, key in [("Mes annonces", "annonces"), ("Mes locations", "locations"), ("Avis reçus", "avis")]:
            b = tk.Button(tabs, text=label, font=("Helvetica", 11), relief="flat", cursor="hand2", padx=20, pady=8,
                          command=lambda k=key: switch_tab(k)) 
            b.pack(side="left")
            tab_btns[key] = b

        tk.Frame(self.root, bg="#D1D5DB", height=1).pack(fill="x")

        main_container = tk.Frame(self.root, bg="#F4F6F8")
        main_container.pack(fill="both", expand=True, padx=20, pady=16)

        canvas = tk.Canvas(main_container, bg="#F4F6F8", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        body_frame = tk.Frame(canvas, bg="#F4F6F8")

        body_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=body_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            bbox = canvas.bbox("all")
            if bbox and bbox[3] > canvas.winfo_height():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        switch_tab("annonces")

        self.root.mainloop()
        self.root.destroy()
    
    def creationAnnonceWindow(self, id):
        self.root = tk.Tk()
        self.root.geometry("600x650")
        self.root.title("EcoLend - Publier une annonce")
        self.root.configure(bg="#F4F6F8")

        cats_db = self.db.s_query("SELECT id, name FROM categories", ret=True)
        # On crée un dictionnaire pour lier le nom de la catégorie à son ID
        cat_dict = {c[1]: c[0] for c in (cats_db or [])}
        cat_names = list(cat_dict.keys())
        if not cat_dict:
            cat_dict = {
                "Outillage": 1,
                "Jardinage": 2,
                "Sport & Loisirs": 3,
                "Électronique": 4,
                "Mobilier": 5,
                "Autre": 6
            }
            
        cat_names = list(cat_dict.keys())

        # Variables du formulaire
        titreVar = tk.StringVar(self.root)
        catVar = tk.StringVar(self.root)
        etatVar = tk.StringVar(self.root)

        def annuler():
            self.action_id = 7 # Retour vers le profil
            self.root.quit()

        def valider():
            titre = titreVar.get().strip()
            categorie_name = catVar.get()
            etat = etatVar.get()
            description = descText.get("1.0", tk.END).strip()

            if not titre or not categorie_name or not etat or not description:
                messagebox.showwarning("Formulaire incomplet", "Veuillez remplir tous les champs.")
                return

            try:
                # On récupère l'ID de la catégorie choisie
                cat_id = cat_dict[categorie_name]
                
                # Insertion dans la base de données
                query = """
                    INSERT INTO listings (user_id, category_id, title, description, tool_condition, status) 
                    VALUES (%s, %s, %s, %s, %s, 'active')
                """
                self.db.c_query(query, (id, cat_id, titre, description, etat), ret=False)
                
                messagebox.showinfo("Succès", "Ton objet a bien été ajouté au catalogue !")
                self.action_id = 7 # Retour vers le profil pour voir l'annonce apparaître
                self.root.quit()
                
            except Exception as e:
                messagebox.showerror("Erreur BDD", f"Impossible de publier l'annonce.\nErreur : {e}")

        topbar = tk.Frame(self.root, bg="#2D6A4F", padx=16, pady=10)
        topbar.pack(fill="x")
        tk.Button(topbar, text="← Annuler", bg="#2D6A4F", fg="#B7E4C7", relief="flat", font=("Helvetica", 11), cursor="hand2", command=annuler).pack(side="left")
        tk.Label(topbar, text=" Nouvelle Annonce", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#2D6A4F").pack(side="left", padx=16)

        form_frame = tk.Frame(self.root, bg="#FFFFFF", padx=40, pady=30, relief="flat", bd=1)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(form_frame, text="Que souhaitez-vous proposer ?", font=("Helvetica", 16, "bold"), bg="#FFFFFF", fg="#1B1B2F").pack(pady=(0, 20), anchor="w")

        # Champ : Titre
        tk.Label(form_frame, text="Titre de l'objet :", font=("Helvetica", 11, "bold"), bg="#FFFFFF", fg="#6B7280").pack(anchor="w")
        tk.Entry(form_frame, textvariable=titreVar, font=("Helvetica", 11), bg="#F4F6F8", relief="flat").pack(fill="x", ipady=6, pady=(5, 15))

        # Champ : Catégorie
        tk.Label(form_frame, text="Catégorie :", font=("Helvetica", 11, "bold"), bg="#FFFFFF", fg="#6B7280").pack(anchor="w")
        from tkinter import ttk
        cat_cb = ttk.Combobox(form_frame, textvariable=catVar, values=cat_names, state="readonly", font=("Helvetica", 11))
        cat_cb.pack(fill="x", ipady=4, pady=(5, 15))

        # Champ : État de l'objet
        tk.Label(form_frame, text="État de l'objet :", font=("Helvetica", 11, "bold"), bg="#FFFFFF", fg="#6B7280").pack(anchor="w")
        etats = ["Neuf", "Très bon", "Bon", "Satisfaisant", "Usé"]
        etat_cb = ttk.Combobox(form_frame, textvariable=etatVar, values=etats, state="readonly", font=("Helvetica", 11))
        etat_cb.pack(fill="x", ipady=4, pady=(5, 15))

        # Champ : Description
        tk.Label(form_frame, text="Description détaillée :", font=("Helvetica", 11, "bold"), bg="#FFFFFF", fg="#6B7280").pack(anchor="w")
        descText = tk.Text(form_frame, font=("Helvetica", 11), bg="#F4F6F8", relief="flat", height=6)
        descText.pack(fill="x", pady=(5, 20))

        # Bouton Valider
        tk.Button(form_frame, text="Publier l'annonce", bg="#52B788", fg="#FFFFFF", relief="flat", font=("Helvetica", 12, "bold"), cursor="hand2", pady=10, command=valider).pack(fill="x")

        self.root.mainloop()
        self.root.destroy()

    def detailAnnonceWindow(self, annonce_id):
        self.root = tk.Tk()
        self.root.title("P2IP - Détails de l'annonce")
        self.root.geometry(self.size)
        self.root.configure(bg="#F4F6F8")

        # 1. Récupération des données de l'annonce spécifique
        query = """
            SELECT L.title, C.name, U.city, L.tool_condition, L.description, U.firstname
            FROM listings L
            JOIN categories C ON L.category_id = C.id
            JOIN users U ON L.user_id = U.id
            WHERE L.id = %s
        """
        result = self.db.c_query(query, (annonce_id), ret=True)
        if not result:
            self.action_id = -1 # Retour sécurité si l'annonce n'existe plus
            self.root.quit()
            return
            
        titre, categorie, ville, etat, description, proprietaire = result[0]

        # 2. Fonctions des boutons
        def go_back():
            self.action_id = -1 # Retour à l'accueil
            self.root.quit()

        def reserver():
            # Fenêtre popup de confirmation OUI / NON
            confirm = messagebox.askyesno("Confirmation", "Êtes-vous certain de vouloir réserver cet objet ?")
            if confirm:
                # Si OUI, on met à jour le statut dans la base de données
                update_query = "UPDATE listings SET status = 'réservé' WHERE id = %s"
                self.db.c_query(update_query, (self.selected_annonce_id,), ret=False)
                
                messagebox.showinfo("Succès", "L'objet a bien été réservé !")
                self.action_id = 2 # Retour à l'accueil pour constater qu'il a disparu
                self.root.destroy()

        # 3. Construction de l'interface
        topbar = tk.Frame(self.root, bg="#2D6A4F", padx=16, pady=10)
        topbar.pack(fill="x")
        tk.Button(topbar, text="← Retour", bg="#2D6A4F", fg="#B7E4C7", relief="flat", font=("Helvetica", 11), cursor="hand2", command=go_back).pack(side="left")
        tk.Label(topbar, text=" Détails de l'objet", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#2D6A4F").pack(side="left", padx=16)

        body = tk.Frame(self.root, bg="#F4F6F8", padx=40, pady=20)
        body.pack(fill="both", expand=True)

        # Espace pour une future photo
        photo_frame = tk.Frame(body, bg="#D1D5DB", width=400, height=250)
        photo_frame.pack(pady=10)
        photo_frame.pack_propagate(False)
        tk.Label(photo_frame, text="[Emplacement Photo de l'objet]", bg="#D1D5DB", fg="#6B7280", font=("Helvetica", 12, "italic")).pack(expand=True)

        # Informations principales
        tk.Label(body, text=titre, font=("Helvetica", 20, "bold"), bg="#F4F6F8", fg="#1B1B2F").pack(pady=(15, 5))
        info_text = f"🏷️ Catégorie : {categorie}   |   📍 Lieu : {ville}   |   ⭐ État : {etat}\n👤 Proposé par : {proprietaire}"
        tk.Label(body, text=info_text, font=("Helvetica", 12), bg="#F4F6F8", fg="#6B7280").pack(pady=5)

        # Description
        desc_frame = tk.Frame(body, bg="#FFFFFF", padx=20, pady=15, relief="flat", bd=1)
        desc_frame.pack(fill="x", pady=20)
        tk.Label(desc_frame, text="Description :", font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg="#1B1B2F").pack(anchor="w")
        tk.Label(desc_frame, text=description, font=("Helvetica", 11), bg="#FFFFFF", fg="#6B7280", wraplength=600, justify="left").pack(anchor="w", pady=5)

        # Bouton d'action
        tk.Button(body, text="💳 Réserver cet objet", bg="#52B788", fg="#FFFFFF", font=("Helvetica", 13, "bold"), relief="flat", cursor="hand2", padx=20, pady=10, command=reserver).pack(pady=10)

        self.root.mainloop()
        self.root.destroy()