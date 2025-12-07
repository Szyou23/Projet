"""
Panel administrateur
"""
import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
import ui

def show_admin_dashboard(main_frame, go_users_callback, go_offres_callback):
    pass