import tkinter as tk
from tkinter import messagebox
import ctypes as ct

class UI():
    def __init__(self, db_handler):
        self.root = None
        self.size = "600x400"
        self.color = "000000"
        self.action_id = None
        self.icon = "ressources/main_icon.ico"
        self.progress = None
        self.db = db_handler
        self.current_user_id = 1
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

        iLogo = tk.PhotoImage(file = "ressources/main_icon.png")
        iLogo = iLogo.subsample(2, 2)
        iLogoLabel = tk.Label(master = self.root, image = iLogo)
        iLogoLabel.pack(anchor = 'n')

        uVar = tk.StringVar()
        uEntry = tk.Entry(self.root, width = 40, textvariable = uVar, bg = "#DBD9D9", fg = "black")
        uEntry.place_configure(relx = 0.255, rely = 0.48)

        pVar = tk.StringVar()
        pEntry = tk.Entry(self.root, width = 40, textvariable = pVar, bg = "#DBD9D9", fg = "black")
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
        les tests sur les infos se font dans le main, après la fin de la fenêtre (genre nom et prénom non nuls, email unique, pwd respectant la stratégie, etc...)"""
        None

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

    def accueilWindow(self):
        """
        fenêtre d'acceuil qui affiche les annonces actuelles, sur laquelle est branché le programme après connection / creation de compte
        """
        self.root = tk.Tk()
        self.root.title("P2IP - Accueil & Recherche")
        self.root.geometry(self.size)
        self.root.configure(bg="#F4F6F8")

        cats_db = self.db.s_query("SELECT name FROM Categories", ret=True)
        CATEGORIES = ["Toutes"] + [c[0] for c in (cats_db or [])]

        query_annonces = """
            SELECT L.id, L.title, L.description, C.name, U.city 
            FROM Listings L
            JOIN Categories C ON L.category_id = C.id
            JOIN Users U ON L.user_id = U.id
            WHERE L.status = 'disponible'
        """
        annonces_db = self.db.s_query(query_annonces, ret=True)
        
        self.search_var = tk.StringVar(self.root)
        self.cat_var = tk.StringVar(self.root, value="Toutes")

        def go_to_profil():
            self.action_id = 0
            self.root.quit()
            
        def go_to_liste_annonces():
            self.action_id = 1
            self.root.quit()

        topbar = tk.Frame(self.root, bg="#2D6A4F", padx=16, pady=10)
        topbar.pack(fill="x")

        tk.Label(topbar, text=" P2IP", font=("Helvetica", 18, "bold"), fg="#FFFFFF", bg="#2D6A4F").pack(side="left")

        tk.Button(topbar, text=" Mon profil", bg="#B7E4C7", fg="#2D6A4F", relief="flat",
                  command=go_to_profil).pack(side="right")

        tk.Button(topbar, text="Rechercher (Voir Liste)", bg="#52B788", fg="#FFFFFF", relief="flat",
                  command=go_to_liste_annonces).pack(side="right", padx=10)

        body = tk.Frame(self.root, bg="#F4F6F8")
        body.pack(fill="both", expand=True, padx=16, pady=12)
        
        tk.Label(body, text="Annonces récentes :", font=("Helvetica", 14, "bold"), bg="#F4F6F8").pack(anchor="w")
        
        if annonces_db:
            for annonce in annonces_db:
                texte = f"{annonce[1]} (Catégorie: {annonce[3]}) - à {annonce[4]}"
                tk.Label(body, text=texte, font=("Helvetica", 11), bg="#FFFFFF", pady=5).pack(fill="x", pady=2)
        else:
            tk.Label(body, text="Aucune annonce en base de données.", bg="#F4F6F8").pack()

        self.root.mainloop()
        self.root.destroy()

    def listeAnnoncesWindow(self):
        self.root = tk.Tk()
        self.root.title("P2IP – Liste des annonces")
        self.root.geometry(self.size) 
        self.root.configure(bg="#F4F6F8")

        def go_back():
            self.action_id = 2 
            self.root.quit()

        def apply_filters(*args):
            print("Filtrage à implémenter dynamiquement !")

        query = """
            SELECT L.title, C.name, U.city, L.tool_condition, L.description
            FROM Listings L
            JOIN Categories C ON L.category_id = C.id
            JOIN Users U ON L.user_id = U.id
            WHERE L.status = 'disponible'
        """
        annonces = self.db.s_query(query, ret=True)

        topbar = tk.Frame(self.root, bg="#2D6A4F", padx=16, pady=10)
        topbar.pack(fill="x")

        tk.Button(topbar, text="← Retour", bg="#2D6A4F", fg="#B7E4C7", relief="flat",
                  font=("Helvetica", 11), cursor="hand2", command=go_back).pack(side="left")
        tk.Label(topbar, text=" P2IP - Catalogue", font=("Helvetica", 16, "bold"),
                 fg="#FFFFFF", bg="#2D6A4F").pack(side="left", padx=16)

        container = tk.Frame(self.root, bg="#F4F6F8")
        container.pack(fill="both", expand=True, padx=16, pady=12)

        tk.Label(container, text=f"{len(annonces) if annonces else 0} annonce(s) trouvée(s)", 
                 font=("Helvetica", 11, "bold"), bg="#F4F6F8").pack(anchor="w", pady=(0, 10))

        if annonces:
            for a in annonces:
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
        else:
            tk.Label(container, text="Aucune annonce ne correspond à votre recherche.", bg="#F4F6F8", fg="#6B7280").pack()

        self.root.mainloop()
        self.root.destroy()

    def profilWindow(self):
        self.root = tk.Tk()
        self.root.title("P2IP – Mon Profil") 
        self.root.geometry(self.size)
        self.root.configure(bg="#F4F6F8") 

        user_data = self.db.c_query(
            "SELECT firstname, lastname, city FROM Users WHERE id = %s", 
            (self.current_user_id,), 
            ret=True
        )
        
        prenom, nom, ville = ("Utilisateur", "Inconnu", "Non renseignée")
        if user_data:
            prenom, nom, ville = user_data[0]

        query_annonces = """
            SELECT L.title, C.name, L.status 
            FROM Listings L
            JOIN Categories C ON L.category_id = C.id
            WHERE L.user_id = %s
        """
        mes_annonces_db = self.db.c_query(query_annonces, (self.current_user_id,), ret=True)

        self.active_tab = tk.StringVar(self.root, value="annonces") 

        def go_back():
            self.action_id = 2
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
                      command=lambda: messagebox.showinfo("Navigation", "→ Formulaire de publication")).pack(anchor="e", pady=(0, 12))
            
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

        body_frame = tk.Frame(self.root, bg="#F4F6F8")
        body_frame.pack(fill="both", expand=True, padx=20, pady=16) 

        switch_tab("annonces")

        self.root.mainloop()
        self.root.destroy()