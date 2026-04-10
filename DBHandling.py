import pymysql as p
import pymysql.err as er
import os

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
    
    def s_query(self, query: str, ret: bool):
        """
        executes a simple query on the database\n
        les simple query ne prennent pas en charge les variables dynamiques
        """
        self.cursor.execute(query)
        self.cnx.commit()
        if ret:
            return self.cursor.fetchall()

    def c_query(self, query: str, dynamic: tuple[str], ret: bool):
        """
        exécutes une query dite complexe\n
        - dynamic est un tuple de string qui contient les values utiles dans la requête
        - pas oublier de placer les %s à la place des valeurs à utiliser dans dynamic
        """
        self.cursor.execute(query, dynamic)
        self.cnx.commit()
        if ret:
            return self.cursor.fetchall()
    
    def show_tables(self) -> None:
        """
        Simple method to make sure that the tables in the database are all present
        """
        self.cursor.execute("SHOW TABLES;")
        tables = self.cursor.fetchall()

        for table in tables:
            print(table[0])
    
    def clear():
        """
        Just clears the command prompt based on what os is currently used. 
        """
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")