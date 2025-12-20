import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
import ui

def show_admin_dashboard(main_frame, go_users_callback, go_offres_callback):
    #Tableau de bord administrateur
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Header
    headerFrame = tk.Frame(main_frame, bg=COULEURS["admin"], height=150)
    headerFrame.pack(fill="x")
    
    tk.Label(
        headerFrame,
        text="⚙️ Tableau de bord Administrateur",
        font=("Arial", 24, "bold"),
        bg=COULEURS["admin"],
        fg=COULEURS["white"]
    ).pack(pady=50)
    
    # Statistiques
    statsFrame = tk.Frame(main_frame, bg=COULEURS["light_bg"])
    statsFrame.pack(fill="both", expand=True, pady=20)
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE type_utilisateur != 'admin'")
            nb_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE type_utilisateur = 'recruteur'")
            nb_recruteurs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE type_utilisateur = 'chercheur'")
            nb_chercheurs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM offres_emploi")
            nb_offres = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            statsContainer = tk.Frame(statsFrame, bg=COULEURS["white"], width=500)
            statsContainer.place(relx=0.5, rely=0.2, anchor="center")
            
            tk.Label(
                statsContainer,
                text="📊 Statistiques de la plateforme",
                font=("Arial", 18, "bold"),
                bg=COULEURS["white"],
                fg=COULEURS["admin"]
            ).pack(pady=20)
            
            stats_data = [
                ("👥 Total utilisateurs", nb_users, COULEURS["primary"]),
                ("💼 Recruteurs", nb_recruteurs, COULEURS["warning"]),
                ("🔍 Chercheurs d'emploi", nb_chercheurs, COULEURS["success"]),
                ("📋 Offres d'emploi", nb_offres, COULEURS["accent"])
            ]
            
            for label, value, color in stats_data:
                statFrame = tk.Frame(statsContainer, bg=COULEURS["white"])
                statFrame.pack(fill="x", padx=40, pady=10)
                
                tk.Label(
                    statFrame,
                    text=label,
                    font=("Arial", 12, "bold"),
                    bg=COULEURS["white"],
                    fg=COULEURS["dark"],
                    width=25,
                    anchor="w"
                ).pack(side="left")
                
                tk.Label(
                    statFrame,
                    text=str(value),
                    font=("Arial", 14, "bold"),
                    bg=COULEURS["white"],
                    fg=color
                ).pack(side="right")
            
            tk.Frame(statsContainer, bg=COULEURS["light_bg"], height=2).pack(fill="x", padx=40, pady=20)
            
            tk.Button(
                statsContainer,
                text="👥 Gérer les utilisateurs",
                font=("Arial", 12, "bold"),
                bg=COULEURS["primary"],
                fg=COULEURS["white"],
                width=30,
                height=2,
                cursor="hand2",
                bd=0,
                command=go_users_callback
            ).pack(pady=10)
            
            tk.Button(
                statsContainer,
                text="💼 Gérer les offres d'emploi",
                font=("Arial", 12, "bold"),
                bg=COULEURS["success"],
                fg=COULEURS["white"],
                width=30,
                height=2,
                cursor="hand2",
                bd=0,
                command=go_offres_callback
            ).pack(pady=10)
            
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur de chargement des statistiques: {e}")