import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
import ui

def show_profil(main_frame, go_connexion_callback, go_inscription_callback, go_accueil_callback):
    """Affiche le profil de l'utilisateur"""
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    current_user, user_type = ui.get_current_user()

    if not current_user:
        container = tk.Frame(main_frame, bg=COULEURS["white"], width=400, height=300)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            container,
            text="Veuillez vous connecter",
            font=("Arial", 18, "bold"),
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
        
        tk.Button(
            container,
            text="S'inscrire",
            font=("Arial", 12, "bold"),
            bg=COULEURS["white"],
            fg=COULEURS["primary"],
            width=20,
            height=2,
            cursor="hand2",
            bd=2,
            relief="solid",
            command=go_inscription_callback
        ).pack(pady=10)
        return

    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nom, email, date_creation, type_utilisateur FROM utilisateurs WHERE email = %s", (current_user,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            nom, email, date_creation, type_user = user
            
            container = tk.Frame(main_frame, bg=COULEURS["white"], width=500, height=600)
            container.place(relx=0.5, rely=0.5, anchor="center")
            
            # En-tête du profil
            header_color = COULEURS["admin"] if type_user == "admin" else COULEURS["primary"]
            headerFrame = tk.Frame(container, bg=header_color, width=500, height=120)
            headerFrame.pack(fill="x")
            
            icon = "⚙️" if type_user == "admin" else ("💼" if type_user == "recruteur" else "🔍")
            tk.Label(
                headerFrame,
                text=icon,
                font=("Arial", 40),
                bg=header_color,
                fg=COULEURS["white"]
            ).pack(pady=20)
            
            # Informations
            infoFrame = tk.Frame(container, bg=COULEURS["white"])
            infoFrame.pack(pady=20, padx=40, fill="both", expand=True)
            
            tk.Label(
                infoFrame,
                text="Informations du profil",
                font=("Arial", 18, "bold"),
                bg=COULEURS["white"],
                fg=COULEURS["primary"]
            ).pack(pady=(0, 20))
            
            # Nom
            tk.Label(infoFrame, text="Nom complet", font=("Arial", 10),
                    bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w")
            tk.Label(infoFrame, text=nom, font=("Arial", 13, "bold"),
                    bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", pady=(0, 15))
            
            # Email
            tk.Label(infoFrame, text="Adresse email", font=("Arial", 10),
                    bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w")
            tk.Label(infoFrame, text=email, font=("Arial", 13, "bold"),
                    bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", pady=(0, 15))
            
            # Type de compte
            tk.Label(infoFrame, text="Type de compte", font=("Arial", 10),
                    bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w")
            
            if type_user == "admin":
                type_display = "⚙️ Administrateur"
                type_color = COULEURS["admin"]
            elif type_user == "recruteur":
                type_display = "💼 Recruteur"
                type_color = COULEURS["warning"]
            else:
                type_display = "🔍 Chercheur d'emploi"
                type_color = COULEURS["success"]
            
            tk.Label(infoFrame, text=type_display, font=("Arial", 13, "bold"),
                    bg=COULEURS["white"], fg=type_color).pack(anchor="w", pady=(0, 15))
            
            # Date de création
            tk.Label(infoFrame, text="Membre depuis", font=("Arial", 10),
                    bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w")
            tk.Label(infoFrame, text=date_creation.strftime("%d/%m/%Y"), font=("Arial", 13, "bold"),
                    bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", pady=(0, 30))
            
            # Bouton déconnexion
            def deconnecter():
                ui.logout_user()
                messagebox.showinfo("Déconnexion", "Vous avez été déconnecté avec succès !")
                go_accueil_callback()
            
            tk.Button(
                infoFrame,
                text="Se déconnecter",
                font=("Arial", 12, "bold"),
                bg=COULEURS["danger"],
                fg=COULEURS["white"],
                width=30,
                height=2,
                cursor="hand2",
                bd=0,
                command=deconnecter
            ).pack(pady=10)
    except Error as e:
        messagebox.showerror("Erreur", f"Erreur de chargement du profil: {e}")