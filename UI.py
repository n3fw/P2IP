import tkinter as tk
from PIL import ImageTk


class UI():
    def __init__(self):
        self.root = None
        self.size = "1200x1000"
        self.color = "000000"
        self.action_id = None
        self.icon = "ressources/main_icon.ico"
        self.progress = None
    
    def connexionWindow(self):
        self.root = tk.Tk()
