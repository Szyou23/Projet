import tkinter as tk
from tkinter import messagebox, ttk
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
from utils import hash_password
import ui

def show_parametres(main_frame, go_connexion_callback, go_accueil_callback):
    """Affiche les paramètres du compte/utilisateur"""
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    current_user, user_type = ui.get_current_user()
    
    if not current_user:
        container = tk.Frame(main_frame, bg=COULEURS["white"], width=400, height=300)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            container,
            text="Veuillez vous connecter pour accéder aux paramètres",
            font=("Arial", 14, "bold"),
            bg=COULEURS["white"],
            fg=COULEURS["primary"],
            wraplength=350,
            justify="center"
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

    container = tk.Frame(main_frame, bg=COULEURS["white"], width=550, height=600)
    container.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(
        container,
        text="Paramètres du compte",
        font=("Arial", 24, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"]
    ).pack(pady=20)
    
    tk.Label(
        container,
        text="Gérez votre compte JobFinder",
        font=("Arial", 12),
        bg=COULEURS["white"],
        fg=COULEURS["dark"]
    ).pack(pady=(0, 20))


    frame_mdp = tk.LabelFrame(
        container,
        text="Changer le mot de passe",
        font=("Arial", 11, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"],
        bd=2,
        relief="groove",
        labelanchor="nw"
    )
    frame_mdp.pack(padx=40, pady=15, fill="x")

    tk.Label(
        frame_mdp,
        text="Ancien mot de passe",
        font=("Arial", 10),
        bg=COULEURS["white"],
        fg=COULEURS["dark"]
    ).pack(anchor="w", padx=15, pady=(10, 2))
    entry_old = tk.Entry(frame_mdp, show="●", width=35, font=("Arial", 10), bd=2, relief="groove")
    entry_old.pack(padx=15, pady=(0, 10))

    tk.Label(
        frame_mdp,
        text="Nouveau mot de passe (min. 6 caractères)",
        font=("Arial", 10),
        bg=COULEURS["white"],
        fg=COULEURS["dark"]
    ).pack(anchor="w", padx=15, pady=(0, 2))
    entry_new = tk.Entry(frame_mdp, show="●", width=35, font=("Arial", 10), bd=2, relief="groove")
    entry_new.pack(padx=15, pady=(0, 10))

    tk.Label(
        frame_mdp,
        text="Confirmer le nouveau mot de passe",
        font=("Arial", 10),
        bg=COULEURS["white"],
        fg=COULEURS["dark"]
    ).pack(anchor="w", padx=15, pady=(0, 2))
    entry_new2 = tk.Entry(frame_mdp, show="●", width=35, font=("Arial", 10), bd=2, relief="groove")
    entry_new2.pack(padx=15, pady=(0, 10))

    def changer_mdp():
        old = entry_old.get()
        new = entry_new.get()
        new2 = entry_new2.get()

        if not old or not new or not new2:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs de mot de passe.")
            return
        if len(new) < 6:
            messagebox.showerror("Erreur", "Le nouveau mot de passe doit contenir au moins 6 caractères.")
            return
        if new != new2:
            messagebox.showerror("Erreur", "Les nouveaux mots de passe ne correspondent pas.")
            return

        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT mot_de_passe FROM utilisateurs WHERE email=%s",
                (current_user,)
            )
            row = cursor.fetchone()
            if not row:
                cursor.close()
                conn.close()
                messagebox.showerror("Erreur", "Utilisateur introuvable.")
                return

            old_hash = hash_password(old)
            if row[0] != old_hash:
                cursor.close()
                conn.close()
                messagebox.showerror("Erreur", "Ancien mot de passe incorrect.")
                return

            new_hash = hash_password(new)
            cursor.execute(
                "UPDATE utilisateurs SET mot_de_passe=%s WHERE email=%s",
                (new_hash, current_user)
            )
            conn.commit()
            cursor.close()
            conn.close()

            entry_old.delete(0, "end")
            entry_new.delete(0, "end")
            entry_new2.delete(0, "end")

            messagebox.showinfo("Succès", "Mot de passe modifié avec succès.")
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du mot de passe : {e}")

    tk.Button(
        frame_mdp,
        text="Modifier le mot de passe",
        font=("Arial", 11, "bold"),
        bg=COULEURS["primary"],
        fg=COULEURS["white"],
        width=25,
        height=1,
        cursor="hand2",
        bd=0,
        command=changer_mdp
    ).pack(pady=10)

    if user_type == "admin":
        frame_type = tk.LabelFrame(
            container,
            text="Gestion du type de compte (Admin)",
            font=("Arial", 11, "bold"),
            bg=COULEURS["white"],
            fg=COULEURS["admin"],
            bd=2,
            relief="groove",
            labelanchor="nw"
        )
        frame_type.pack(padx=40, pady=15, fill="x")

        tk.Label(
            frame_type,
            text="Changer le type de compte d'un utilisateur (recruteur/chercheur)",
            font=("Arial", 10),
            bg=COULEURS["white"],
            fg=COULEURS["dark"],
            wraplength=430,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        tk.Label(
            frame_type,
            text="Email de l'utilisateur",
            font=("Arial", 10),
            bg=COULEURS["white"],
            fg=COULEURS["dark"]
        ).pack(anchor="w", padx=15, pady=(0, 2))
        entry_email = tk.Entry(frame_type, width=35, font=("Arial", 10), bd=2, relief="groove")
        entry_email.pack(padx=15, pady=(0, 8))

        tk.Label(
            frame_type,
            text="Nouveau type de compte",
            font=("Arial", 10),
            bg=COULEURS["white"],
            fg=COULEURS["dark"]
        ).pack(anchor="w", padx=15, pady=(0, 2))

        type_var = tk.StringVar(value="chercheur")
        combo_type = ttk.Combobox(frame_type, textvariable=type_var, width=33, font=("Arial", 10), state="readonly")
        combo_type['values'] = ("recruteur", "chercheur")
        combo_type.current(1)
        combo_type.pack(padx=15, pady=(0, 10))

        def changer_type():
            email = entry_email.get().strip()
            nouveau_type = type_var.get()

            if not email:
                messagebox.showerror("Erreur", "Veuillez saisir l'email de l'utilisateur.")
                return

            conn = get_db_connection()
            if not conn:
                return

            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, type_utilisateur FROM utilisateurs WHERE email=%s",
                    (email,)
                )
                row = cursor.fetchone()
                if not row:
                    cursor.close()
                    conn.close()
                    messagebox.showerror("Erreur", "Aucun utilisateur trouvé avec cet email.")
                    return

                if row[1] == "admin":
                    cursor.close()
                    conn.close()
                    messagebox.showerror("Erreur", "Vous ne pouvez pas modifier le type d'un administrateur.")
                    return

                cursor.execute(
                    "UPDATE utilisateurs SET type_utilisateur=%s WHERE id=%s",
                    (nouveau_type, row[0])
                )
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Succès", f"Type de compte mis à jour en '{nouveau_type}'.")
                entry_email.delete(0, "end")

            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du type de compte : {e}")

        tk.Button(
            frame_type,
            text="Mettre à jour le type de compte",
            font=("Arial", 11, "bold"),
            bg=COULEURS["admin"],
            fg=COULEURS["white"],
            width=28,
            height=1,
            cursor="hand2",
            bd=0,
            command=changer_type
        ).pack(pady=10)

    tk.Button(
        container,
        text="⬅️ Retour",
        font=("Arial", 12, "bold"),
        bg=COULEURS["primary"],
        fg=COULEURS["white"],
        width=20,
        height=2,
        cursor="hand2",
        bd=0,
        command=go_accueil_callback
    ).pack(pady=20)