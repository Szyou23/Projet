import tkinter as tk
from tkinter import messagebox
from config import COULEURS
from utils import valider_email
import ui

def show_inscription(main_frame, go_profil_callback, go_connexion_callback):
    """Affiche la page d'inscription avec choix du type d'utilisateur"""
    for widget in main_frame.winfo_children():
        widget.destroy()

    container = tk.Frame(main_frame, bg=COULEURS["white"], width=450, height=650)
    container.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        container,
        text="Créer un compte",
        font=("Arial", 24, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"]
    ).pack(pady=20)

    # Nom
    tk.Label(container, text="Nom complet", font=("Arial", 11),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    entryNom = tk.Entry(container, width=35, font=("Arial", 11), bd=2, relief="groove")
    entryNom.pack(pady=(5, 15), padx=40)

    # Email avec indicateur de validation
    emailFrame = tk.Frame(container, bg=COULEURS["white"])
    emailFrame.pack(fill="x", padx=40)
    
    tk.Label(emailFrame, text="Adresse email", font=("Arial", 11),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w")
    
    emailValidLabel = tk.Label(emailFrame, text="", font=("Arial", 9),
                              bg=COULEURS["white"])
    emailValidLabel.pack(anchor="e")
    
    entryEmail = tk.Entry(container, width=35, font=("Arial", 11), bd=2, relief="groove")
    entryEmail.pack(pady=(5, 15), padx=40)
    
    # Fonction de validation en temps réel
    def valider_email_temps_reel(event=None):
        email = entryEmail.get().strip()
        if not email:
            emailValidLabel.config(text="", fg=COULEURS["dark"])
        elif valider_email(email):
            emailValidLabel.config(text="✓ Email valide", fg=COULEURS["success"])
            entryEmail.config(bg="white")
        else:
            emailValidLabel.config(text="✗ Format invalide", fg=COULEURS["danger"])
            entryEmail.config(bg="#ffebee")
    
    entryEmail.bind("<KeyRelease>", valider_email_temps_reel)

    # Mot de passe
    tk.Label(container, text="Mot de passe (min. 6 caractères)", font=("Arial", 11),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    entryMDP = tk.Entry(container, show="●", width=35, font=("Arial", 11), bd=2, relief="groove")
    entryMDP.pack(pady=(5, 20), padx=40)

    # Séparateur
    tk.Frame(container, bg=COULEURS["light_bg"], height=2).pack(fill="x", padx=40, pady=15)
    
    tk.Label(
        container,
        text="Type de compte",
        font=("Arial", 12, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"]
    ).pack(pady=10)

    # Choix du type d'utilisateur avec RadioButton
    type_var = tk.StringVar(value="chercheur")

    radioFrame = tk.Frame(container, bg=COULEURS["white"])
    radioFrame.pack(pady=10)

    # Option Chercheur
    chercheurFrame = tk.Frame(radioFrame, bg=COULEURS["white"], bd=2, relief="groove")
    chercheurFrame.pack(pady=5, padx=40, fill="x")
    
    tk.Radiobutton(
        chercheurFrame,
        text="🔍 Chercheur d'emploi",
        variable=type_var,
        value="chercheur",
        font=("Arial", 11, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["dark"],
        activebackground=COULEURS["white"],
        cursor="hand2",
        selectcolor=COULEURS["white"]
    ).pack(anchor="w", padx=10, pady=5)
    
    tk.Label(
        chercheurFrame,
        text="Je cherche un emploi et je veux consulter les offres",
        font=("Arial", 9),
        bg=COULEURS["white"],
        fg=COULEURS["dark"]
    ).pack(anchor="w", padx=30, pady=(0, 5))

    # Option Recruteur
    recruteurFrame = tk.Frame(radioFrame, bg=COULEURS["white"], bd=2, relief="groove")
    recruteurFrame.pack(pady=5, padx=40, fill="x")
    
    tk.Radiobutton(
        recruteurFrame,
        text="💼 Recruteur / Entreprise",
        variable=type_var,
        value="recruteur",
        font=("Arial", 11, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["dark"],
        activebackground=COULEURS["white"],
        cursor="hand2",
        selectcolor=COULEURS["white"]
    ).pack(anchor="w", padx=10, pady=5)
    
    tk.Label(
        recruteurFrame,
        text="Je veux publier des offres d'emploi",
        font=("Arial", 9),
        bg=COULEURS["white"],
        fg=COULEURS["dark"]
    ).pack(anchor="w", padx=30, pady=(0, 5))

    # Bouton s'inscrire
    tk.Button(
        container,
        text="S'inscrire",
        font=("Arial", 12, "bold"),
        bg=COULEURS["primary"],
        fg=COULEURS["white"],
        width=30,
        height=2,
        cursor="hand2",
        bd=0,
        command=lambda: ajouter_utilisateur(
            entryNom.get(), 
            entryEmail.get(), 
            entryMDP.get(),
            type_var.get(),
            go_profil_callback
        )
    ).pack(pady=15)

    # Lien vers connexion
    lienLogin = tk.Label(
        container,
        text="Vous avez déjà un compte ? Se connecter",
        font=("Arial", 10, "underline"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"],
        cursor="hand2"
    )
    lienLogin.pack(pady=10)
    lienLogin.bind("<Button-1>", lambda e: go_connexion_callback())

def ajouter_utilisateur(nom, email, mdp, type_user, go_profil_callback):
    return