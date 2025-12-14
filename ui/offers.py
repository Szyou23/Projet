import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
import ui

def show_offres(main_frame, go_connexion_callback):
    """Affiche les offres selon le type d'utilisateur"""
    current_user, user_type = ui.get_current_user()
    
    # Vérifier si l'utilisateur est connecté
    if not current_user:
        for widget in main_frame.winfo_children():
            widget.destroy()
        
        # Message de connexion requise
        container = tk.Frame(main_frame, bg=COULEURS["white"], width=400, height=300)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            container,
            text="Connectez-vous pour voir les offres",
            font=("Arial", 16, "bold"),
            bg=COULEURS["white"],
            fg=COULEURS["primary"]
        ).pack(pady=30)
        
        tk.Button(
            container,
            text="Se connecter",
            font=("Arial", 12, "bold"),
            bg=COULEURS["primary"],
            fg=COULEURS["white"],
            width=20,
            height=2,
            cursor="hand2",
            bd=0,
            command=go_connexion_callback
        ).pack(pady=10)
        return
    
    # Redirection basique selon le type
    if user_type == "chercheur":
        show_toutes_offres(main_frame)
    elif user_type == "recruteur":
        # TODO: Hna zid show_mes_offres()!
        tk.Label(
            main_frame,
            text="Mes offres - En développement...",
            font=("Arial", 14),
            bg=COULEURS["light_bg"]
        ).pack(pady=50)
    else:
        # Hadi Pour admin
        tk.Label(
            main_frame,
            text="Panel Admin - À venir",
            font=("Arial", 14),
            bg=COULEURS["light_bg"]
        ).pack(pady=50)

def show_toutes_offres(main_frame):
    """Affiche toutes les offres - VERSION SIMPLE"""
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Frame principal
    container = tk.Frame(main_frame, bg=COULEURS["light_bg"])
    container.pack(fill="both", expand=True)
    
    # En-tête simple
    tk.Label(
        container,
        text="🔍 Offres d'emploi disponibles",
        font=("Arial", 20, "bold"),
        bg=COULEURS["success"],
        fg=COULEURS["white"],
        height=3
    ).pack(fill="x")
    
    # Récupération des offres depuis la base de données
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, titre, entreprise, localisation, type_contrat 
                FROM offres_emploi 
                ORDER BY date_creation DESC
            """)
            offres = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if offres:
                for offre in offres:
                    offre_id, titre, entreprise, localisation, type_contrat = offre
                    
                    # Carte basique
                    cardFrame = tk.Frame(container, bg=COULEURS["white"], bd=1, relief="solid")
                    cardFrame.pack(pady=10, padx=50, fill="x")
                    
                    tk.Label(
                        cardFrame,
                        text=titre,
                        font=("Arial", 13, "bold"),
                        bg=COULEURS["white"],
                        fg=COULEURS["primary"]
                    ).pack(anchor="w", padx=15, pady=(10, 5))
                    
                    tk.Label(
                        cardFrame,
                        text=f"{entreprise} - {localisation}",
                        font=("Arial", 10),
                        bg=COULEURS["white"],
                        fg=COULEURS["dark"]
                    ).pack(anchor="w", padx=15)
                    
                    tk.Label(
                        cardFrame,
                        text=type_contrat,
                        font=("Arial", 9),
                        bg=COULEURS["white"],
                        fg="gray"
                    ).pack(anchor="w", padx=15, pady=(0, 10))
            else:
                tk.Label(
                    container,
                    text="Aucune offre disponible",
                    font=("Arial", 12),
                    bg=COULEURS["light_bg"],
                    fg=COULEURS["dark"]
                ).pack(pady=50)
                
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
