# ui/settings.py
"""
Paramètres du compte
"""
import tkinter as tk
from tkinter import messagebox, ttk
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
from utils import hash_password
import ui

def show_parametres(main_frame, go_connexion_callback, go_accueil_callback):
    pass