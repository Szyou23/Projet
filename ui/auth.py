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

    # Bouton S'inscrire
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
<<<<<<< HEAD
    """Ajoute un nouvel utilisateur dans la base de données avec validation d'email"""
    # Validation des champs obligatoires
    if not nom or not email or not mdp or not type_user:
        messagebox.showerror("Erreur", "Tous les champs sont obligatoires !")
        return
    
    # Nettoyer l'email (supprimer les espaces)
    email = email.strip().lower()
    
    # Validation du nom
    if len(nom) < 2:
        messagebox.showerror("Erreur", "Le nom doit contenir au moins 2 caractères !")
        return
    
    # Validation de l'email
    if not valider_email(email):
        messagebox.showerror("Erreur", "Format d'email invalide !\n\nVeuillez saisir une adresse email valide.\nExemple : nom@domaine.com")
        return
    
    # Vérifications supplémentaires pour l'email
    if len(email) > 100:
        messagebox.showerror("Erreur", "L'adresse email est trop longue (max 100 caractères) !")
        return
    
    # Vérifier les domaines recommandés pour les entreprises
    if type_user == "recruteur":
        domaines_publics = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        domaine = email.split('@')[1].lower()
        if domaine in domaines_publics:
            reponse = messagebox.askyesno(
                "Attention",
                f"Vous utilisez une adresse email personnelle ({domaine}).\n\n"
                "Pour un compte recruteur, il est recommandé d'utiliser une adresse email professionnelle.\n\n"
                "Voulez-vous continuer quand même ?"
            )
            if not reponse:
                return
    
    # Validation du mot de passe
    if len(mdp) < 6:
        messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 6 caractères !")
        return
    
    # Recommandation pour un mot de passe fort
    if len(mdp) < 8 or not any(c.isdigit() for c in mdp):
        reponse = messagebox.askyesno(
            "Mot de passe faible",
            "Votre mot de passe semble faible.\n\n"
            "Un mot de passe fort devrait contenir :\n"
            "• Au moins 8 caractères\n"
            "• Des chiffres et des lettres\n\n"
            "Voulez-vous continuer avec ce mot de passe ?"
        )
        if not reponse:
            return

    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Vérifier si l'email existe déjà (double vérification)
        cursor.execute("SELECT email FROM utilisateurs WHERE LOWER(email) = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            messagebox.showerror("Erreur", "Cette adresse email est déjà enregistrée !\n\nVeuillez utiliser une autre adresse email ou vous connecter avec votre compte existant.")
            return
        
        mdp_hash = hash_password(mdp)
        cursor.execute(
            "INSERT INTO utilisateurs (nom, email, mot_de_passe, type_utilisateur) VALUES (%s, %s, %s, %s)",
            (nom, email, mdp_hash, type_user)
        )
        conn.commit()
        cursor.close()
        conn.close()

        type_display = "Recruteur" if type_user == "recruteur" else "Chercheur d'emploi"
        messagebox.showinfo("Succès", f"Bienvenue {nom} !\n\nVotre compte {type_display} a été créé avec succès.\n\nEmail : {email}")
        
        ui.set_current_user(email, type_user)
        go_profil_callback()
    except Error as e:
        if "Duplicate entry" in str(e):
            messagebox.showerror("Erreur", "Cette adresse email est déjà enregistrée !")
        else:
            messagebox.showerror("Erreur", f"Erreur lors de l'inscription: {e}")

=======
    return
>>>>>>> 1168f70 (update)

def show_connexion(main_frame, go_profil_callback, go_admin_callback, go_inscription_callback):
    """Affiche la page de connexion"""
    for widget in main_frame.winfo_children():
        widget.destroy()

    container = tk.Frame(main_frame, bg=COULEURS["white"], width=400, height=450)
    container.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        container,
        text="Bon retour !",
        font=("Arial", 24, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"]
    ).pack(pady=30)

    tk.Label(container, text="Adresse email", font=("Arial", 11),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    entryEmail = tk.Entry(container, width=35, font=("Arial", 11), bd=2, relief="groove")
    entryEmail.pack(pady=(5, 15), padx=40)

    tk.Label(container, text="Mot de passe", font=("Arial", 11),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    entryMDP = tk.Entry(container, show="●", width=35, font=("Arial", 11), bd=2, relief="groove")
    entryMDP.pack(pady=(5, 20), padx=40)
<<<<<<< HEAD

=======
>>>>>>> 1168f70 (update)
    def connecter():
        email = entryEmail.get()
        mdp = entryMDP.get()
        
        if not email or not mdp:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs !")
            return
        
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            mdp_hash = hash_password(mdp)
            cursor.execute(
                "SELECT email, type_utilisateur FROM utilisateurs WHERE email=%s AND mot_de_passe=%s",
                (email, mdp_hash)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                messagebox.showinfo("Connexion", "Connexion réussie !")
                ui.set_current_user(user[0], user[1])
                
                # Redirection selon le type
                if user[1] == "admin":
                    go_admin_callback()
                else:
                    go_profil_callback()
            else:
                messagebox.showerror("Erreur", "Email ou mot de passe incorrect !")
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur de connexion: {e}")

    tk.Button(
        container,
        text="Se connecter",
        font=("Arial", 12, "bold"),
        bg=COULEURS["primary"],
        fg=COULEURS["white"],
        width=30,
        height=2,
        cursor="hand2",
        bd=0,
        command=connecter
    ).pack(pady=10)

    lienInscription = tk.Label(
        container,
        text="Pas encore de compte ? S'inscrire",
        font=("Arial", 10, "underline"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"],
        cursor="hand2"
    )
    lienInscription.pack(pady=20)
    lienInscription.bind("<Button-1>", lambda e: go_inscription_callback())