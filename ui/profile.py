# ui/profile.py
"""
Gestion du profil utilisateur
"""
import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
import ui

def show_profil(main_frame, go_connexion_callback, go_inscription_callback, go_accueil_callback):
    pass