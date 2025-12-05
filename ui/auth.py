# ui/auth.py
"""
Gestion de l'authentification (connexion/inscription)
"""
import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
from utils import hash_password, valider_email
import ui


def show_inscription(main_frame, go_profil_callback, go_connexion_callback):
    pass
def show_connexion(main_frame, go_profil_callback, go_admin_callback, go_inscription_callback):
    pass