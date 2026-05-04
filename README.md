# Consignes pour l'aspect graphique (UI)

1. Chaque fenêtre correspond à une fenêtre (exemple fenêtre des messages correpond à une méthode messWindow)
2. Les fenêtres peuvent utiliser d'autres fonctions annexes si nécéssaire, toute DOIVENT également faire partie de la classe UI
3. Une fenêtre n'utilise pas forcément tous les attraibuts donnés dans la classe UI, mais utilise obligatoirement `self.root` comme base de la fenêtre (cf `__init__(self)`)
4. Pour initialiser une nouvelle fenêtre, au début d'une méthode, utiliser `self.root = tk.Tk()` pour l'initialiser
5. La méthode d'une fenêtre se termine toujours par :
* `self.root.mainloop()` => lance l'affichage de la fenêtre
PUIS
* `self.root.destroy()` à la toute fin pour détruire la fenêtre   
* Note : il peut y avoir des lignes de code entre ces deux lignes, mais il faut respecter cet ordre là
6. `self.action_id` sert à indiquer au programme principal vers quelle autre fenêtre le programme doit pointer. Exemple pratique sur la fenêtre d'accueil au moment de choisir un compte ou de ce connecter : si le user appuie sur créer un compte, placer `self.action_id` à 0, si il souhaite se connecter `self.action_id` va prendre 1, sinon il reste à None. Ainsi le programme principal peut ensuite brancher la fenêtre de création si `self.action_id = 0`, brancher sur la connexion si `self.action_id = 1`, enfin si `self.action_id = None`, le user n'a appuyé sur aucun bouton => il a fermé la fenêtre => on arrête le programme.

PS: petite consigne pour le `self`, il sert à désigner des éléments qui font partie de la classe comme `this` en C++ sauf qu'ici il est nécessaire de le mettre quand on désigne un élément de la classe dans elle-même. Aussi pour mettre un attribut / une methode en privé sur python, on rajoute __ devant leur nom. exemple : `self.name` est un attribut public mais `self.__name` est un attribut privé