import pymysql as p
import pymysql.err as er

#for ease of use
global true
global false 
true = True
false = False

class DBHandler:
    def __init__(self):
        self.cnx: p.connections.Connection = None
        self.cursor: p.cursors.Cursor = None

    def connect_DB(self, pwd: str):
        """
        utilisée pour se connecter une fois à la DB\n
        -> Ne pas utiliser à la fin car déjà appelée dans le @__init__
        """
        self.cnx = p.connect(
            host = "localhost",
            user = "root",
            password = pwd,
            port = 3306,
            charset = "utf8mb4",
            database = "library"
        )

        self.cursor = self.cnx.cursor()
    
    def s_query(self, query: str):
        """
        executes a simple query on the database\n
        les simple query ne prennent pas en charge les variables dynamiques
        """
        self.cursor.execute(query)
        self.cnx.commit()

    def c_query(self, query: str, dynamic: tuple[str]):
        """
        exécutes une query dite complexe\n
        - dynamic est un tuple de string qui contient les values utiles dans la requête
        """
        self.cursor.execute(query, dynamic)
        self.cnx.commit()