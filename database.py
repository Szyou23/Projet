"""
Gestion de la base de données MySQL
"""
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from config import DB_CONFIG
from utils import hash_password

def connexion_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin_py",
            password="admin",  # adapte ton mot de passe
            database="projet"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print("Erreur MySQL:", e)
        return None

def init_db():
    try:
        conn=connexion_mysql()
        if not conn: 
            return 
        cursor=conn.cursor()
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Base de données initialisée avec succès")
    except Error as e:
        print(f"Erreur d'initialisation: {e}")
        messagebox.showerror("Erreur BD", f"Erreur d'initialisation: {e}")

def get_db_connection():
    return connexion_mysql()
