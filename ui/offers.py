import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import webbrowser
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
import ui

def show_offres(main_frame, go_connexion_callback):
    current_user, user_type = get_db_connection()
    
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
<<<<<<< HEAD
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
=======
def voir_offre(main_frame, offre_id):
    current_user, user_type = ui.get_current_user()
    
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.titre, o.entreprise, o.localisation, o.type_contrat, o.salaire, 
                       o.description, o.competences, o.date_creation, u.nom, u.email
                FROM offres_emploi o
                JOIN utilisateurs u ON o.recruteur_id = u.id
                WHERE o.id = %s
            """, (offre_id,))
            offre = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if offre:
                titre, entreprise, localisation, type_contrat, salaire, description, competences, date_creation, recruteur_nom, recruteur_email = offre
                
                canvas = tk.Canvas(main_frame, bg=COULEURS["light_bg"], highlightthickness=0)
                scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
                container = tk.Frame(canvas, bg=COULEURS["white"])
                
                container.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((300, 0), window=container, anchor="n", width=550)
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Header
                headerFrame = tk.Frame(container, bg=COULEURS["primary"], width=550)
                headerFrame.pack(fill="x")
                
                tk.Label(
                    headerFrame,
                    text=titre,
                    font=("Arial", 20, "bold"),
                    bg=COULEURS["primary"],
                    fg=COULEURS["white"],
                    wraplength=500
                ).pack(pady=30, padx=20)
                
                # Informations principales
                infoFrame = tk.Frame(container, bg=COULEURS["white"])
                infoFrame.pack(pady=20, padx=40, fill="x")
                
                info_data = [
                    ("🏢 Entreprise", entreprise),
                    ("📍 Localisation", localisation),
                    ("📋 Type de contrat", type_contrat),
                    ("💰 Salaire", salaire or "Non précisé"),
                    ("📅 Publiée le", date_creation.strftime("%d/%m/%Y")),
                    ("👤 Recruteur", recruteur_nom)
                ]
                
                for label, value in info_data:
                    frameItem = tk.Frame(infoFrame, bg=COULEURS["white"])
                    frameItem.pack(fill="x", pady=5)
                    
                    tk.Label(
                        frameItem,
                        text=label,
                        font=("Arial", 10, "bold"),
                        bg=COULEURS["white"],
                        fg=COULEURS["dark"],
                        width=20,
                        anchor="w"
                    ).pack(side="left")
                    
                    tk.Label(
                        frameItem,
                        text=value,
                        font=("Arial", 11),
                        bg=COULEURS["white"],
                        fg=COULEURS["primary"]
                    ).pack(side="left")
                
                # Séparateur
                tk.Frame(container, bg=COULEURS["light_bg"], height=2).pack(fill="x", pady=20, padx=40)
                
                # Description
                tk.Label(
                    container,
                    text="📄 Description du poste",
                    font=("Arial", 14, "bold"),
                    bg=COULEURS["white"],
                    fg=COULEURS["primary"]
                ).pack(anchor="w", padx=40, pady=(10, 5))
                
                tk.Label(
                    container,
                    text=description,
                    font=("Arial", 11),
                    bg=COULEURS["white"],
                    fg=COULEURS["dark"],
                    wraplength=470,
                    justify="left"
                ).pack(anchor="w", padx=40, pady=(0, 20))
                
                # Compétences
                if competences:
                    tk.Label(
                        container,
                        text="⭐ Compétences requises",
                        font=("Arial", 14, "bold"),
                        bg=COULEURS["white"],
                        fg=COULEURS["primary"]
                    ).pack(anchor="w", padx=40, pady=(10, 5))
                    
                    tk.Label(
                        container,
                        text=competences,
                        font=("Arial", 11),
                        bg=COULEURS["white"],
                        fg=COULEURS["dark"],
                        wraplength=470,
                        justify="left"
                    ).pack(anchor="w", padx=40, pady=(0, 20))
                
                # Contact (uniquement pour chercheurs et admin)
                if user_type == "chercheur" or user_type == "admin":
                    tk.Frame(container, bg=COULEURS["light_bg"], height=2).pack(fill="x", pady=20, padx=40)
                    
                    tk.Label(
                        container,
                        text="📧 Contact",
                        font=("Arial", 14, "bold"),
                        bg=COULEURS["white"],
                        fg=COULEURS["primary"]
                    ).pack(anchor="w", padx=40, pady=(10, 5))
                    
                    contactLabel = tk.Label(
                        container,
                        text=recruteur_email,
                        font=("Arial", 11, "underline"),
                        bg=COULEURS["white"],
                        fg=COULEURS["primary"],
                        cursor="hand2"
                    )
                    contactLabel.pack(anchor="w", padx=40, pady=(0, 20))
                    contactLabel.bind("<Button-1>", lambda e: webbrowser.open(f"mailto:{recruteur_email}"))
                
                # Bouton Retour
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
                    command=lambda: show_offres(main_frame, None)
                ).pack(pady=30)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
def supprimer_offre(main_frame, offre_id):
    """Supprime une offre après confirmation"""
    current_user, user_type = ui.get_current_user()
    
    reponse = messagebox.askyesno(
        "Confirmation",
        "Êtes-vous sûr de vouloir supprimer cette offre ?\nCette action est irréversible."
    )
    
    if reponse:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM offres_emploi WHERE id = %s", (offre_id,))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Succès", "L'offre a été supprimée avec succès !")
                if user_type == "admin":
                    from ui.admin import show_admin_offres
                    show_admin_offres(main_frame)
                else:
                    show_mes_offres(main_frame)
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
def show_mes_offres(main_frame):
    """Affiche et gère les offres du recruteur"""
    current_user, user_type = ui.get_current_user()
    
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    canvas = tk.Canvas(main_frame, bg=COULEURS["light_bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollableFrame = tk.Frame(canvas, bg=COULEURS["light_bg"])
    
    scrollableFrame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((300, 0), window=scrollableFrame, anchor="n", width=550)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def center_window(event=None):
        canvas_width = canvas.winfo_width()
        if canvas.find_all():
            canvas.coords(canvas.find_all()[0], canvas_width // 2, 0)
    
    canvas.bind("<Configure>", center_window)
    
    headerFrame = tk.Frame(scrollableFrame, bg=COULEURS["primary"], height=100)
    headerFrame.pack(fill="x")
    
    tk.Label(
        headerFrame,
        text="💼 Mes offres d'emploi",
        font=("Arial", 22, "bold"),
        bg=COULEURS["primary"],
        fg=COULEURS["white"]
    ).pack(pady=30)
    
    btnFrame = tk.Frame(scrollableFrame, bg=COULEURS["light_bg"])
    btnFrame.pack(pady=20)
    
    tk.Button(
        btnFrame,
        text="➕ Publier une nouvelle offre",
        font=("Arial", 12, "bold"),
        bg=COULEURS["success"],
        fg=COULEURS["white"],
        width=30,
        height=2,
        cursor="hand2",
        bd=0,
       command=lambda: show_ajouter_offre(main_frame)
    ).pack()
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM utilisateurs WHERE email = %s", (current_user,))
            user_id = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT id, titre, entreprise, localisation, type_contrat, salaire, date_creation 
                FROM offres_emploi 
                WHERE recruteur_id = %s 
                ORDER BY date_creation DESC
            """, (user_id,))
            offres = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if offres:
                for offre in offres:
                    offre_id, titre, entreprise, localisation, type_contrat, salaire, date_creation = offre
                    
                    cardFrame = tk.Frame(scrollableFrame, bg=COULEURS["white"], bd=2, relief="groove")
                    cardFrame.pack(pady=10, padx=30, fill="x")
                    
                    tk.Label(
                        cardFrame,
                        text=titre,
                        font=("Arial", 14, "bold"),
                        bg=COULEURS["white"],
                        fg=COULEURS["primary"]
                    ).pack(anchor="w", padx=20, pady=(15, 5))
                    
                    tk.Label(
                        cardFrame,
                        text=f"🏢 {entreprise}",
                        font=("Arial", 11),
                        bg=COULEURS["white"],
                        fg=COULEURS["dark"]
                    ).pack(anchor="w", padx=20)
                    
                    tk.Label(
                        cardFrame,
                        text=f"📍 {localisation} • {type_contrat} • {salaire or 'Salaire non précisé'}",
                        font=("Arial", 10),
                        bg=COULEURS["white"],
                        fg=COULEURS["dark"]
                    ).pack(anchor="w", padx=20, pady=5)
                    
                    tk.Label(
                        cardFrame,
                        text=f"Publiée le {date_creation.strftime('%d/%m/%Y')}",
                        font=("Arial", 9),
                        bg=COULEURS["white"],
                        fg="gray"
                    ).pack(anchor="w", padx=20)
                    
                    btnActionFrame = tk.Frame(cardFrame, bg=COULEURS["white"])
                    btnActionFrame.pack(pady=10, padx=20, fill="x")
                    
                    tk.Button(
                        btnActionFrame,
                        text="👁️ Voir",
                        font=("Arial", 9, "bold"),
                        bg=COULEURS["primary"],
                        fg=COULEURS["white"],
                        cursor="hand2",
                        bd=0,
                        width=12,
                        command=lambda oid=offre_id: voir_offre(main_frame, oid)
                    ).pack(side="left", padx=5)
                    
                    tk.Button(
                        btnActionFrame,
                        text="✏️ Modifier",
                        font=("Arial", 9, "bold"),
                        bg=COULEURS["warning"],
                        fg=COULEURS["white"],
                        cursor="hand2",
                        bd=0,
                        width=12,
                       # command=lambda oid=offre_id: modifier_offre(main_frame, oid)
                    ).pack(side="left", padx=5)
                    
                    tk.Button(
                        btnActionFrame,
                        text="🗑️ Supprimer",
                        font=("Arial", 9, "bold"),
                        bg=COULEURS["danger"],
                        fg=COULEURS["white"],
                        cursor="hand2",
                        bd=0,
                        width=12,
                        command=lambda oid=offre_id: supprimer_offre(main_frame, oid)
                    ).pack(side="left", padx=5)
            else:
                tk.Label(
                    scrollableFrame,
                    text="Vous n'avez pas encore publié d'offres",
                    font=("Arial", 13),
                    bg=COULEURS["light_bg"],
                    fg=COULEURS["dark"]
                ).pack(pady=50)
                
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
def show_ajouter_offre(main_frame):
    """Formulaire pour ajouter une nouvelle offre"""
    current_user, user_type = ui.get_current_user()
    
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    canvas = tk.Canvas(main_frame, bg=COULEURS["light_bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    container = tk.Frame(canvas, bg=COULEURS["white"])
    
    container.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((300, 0), window=container, anchor="n", width=550)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    tk.Label(
        container,
        text="➕ Publier une offre d'emploi",
        font=("Arial", 22, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"]
    ).pack(pady=30)
    
    # Titre
    tk.Label(container, text="Titre du poste *", font=("Arial", 11, "bold"),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    entryTitre = tk.Entry(container, width=50, font=("Arial", 11), bd=2, relief="groove")
    entryTitre.pack(pady=(5, 15), padx=40)
    
    # Entreprise
    tk.Label(container, text="Nom de l'entreprise *", font=("Arial", 11, "bold"),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    entryEntreprise = tk.Entry(container, width=50, font=("Arial", 11), bd=2, relief="groove")
    entryEntreprise.pack(pady=(5, 15), padx=40)
    
    # Localisation
    tk.Label(container, text="Localisation *", font=("Arial", 11, "bold"),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    entryLocalisation = tk.Entry(container, width=50, font=("Arial", 11), bd=2, relief="groove")
    entryLocalisation.pack(pady=(5, 15), padx=40)
    
    # Type de contrat
    tk.Label(container, text="Type de contrat *", font=("Arial", 11, "bold"),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    comboContrat = ttk.Combobox(container, width=48, font=("Arial", 11), state="readonly")
    comboContrat['values'] = ('CDI', 'CDD', 'Stage', 'Freelance', 'Alternance')
    comboContrat.current(0)
    comboContrat.pack(pady=(5, 15), padx=40)
    
    # Salaire
    tk.Label(container, text="Salaire (optionnel)", font=("Arial", 11, "bold"),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    entrySalaire = tk.Entry(container, width=50, font=("Arial", 11), bd=2, relief="groove")
    entrySalaire.pack(pady=(5, 15), padx=40)
    
    # Description
    tk.Label(container, text="Description du poste *", font=("Arial", 11, "bold"),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    textDescription = scrolledtext.ScrolledText(container, width=40, height=6, font=("Arial", 10), bd=2, relief="groove")
    textDescription.pack(pady=(5, 15), padx=40)
    
    # Compétences requises
    tk.Label(container, text="Compétences requises (optionnel)", font=("Arial", 11, "bold"),
             bg=COULEURS["white"], fg=COULEURS["dark"]).pack(anchor="w", padx=40)
    textCompetences = scrolledtext.ScrolledText(container, width=40, height=4, font=("Arial", 10), bd=2, relief="groove")
    textCompetences.pack(pady=(5, 20), padx=40)
    
    def publier():
        titre = entryTitre.get()
        entreprise = entryEntreprise.get()
        localisation = entryLocalisation.get()
        type_contrat = comboContrat.get()
        salaire = entrySalaire.get() or None
        description = textDescription.get("1.0", "end-1c")
        competences = textCompetences.get("1.0", "end-1c") or None
        
        if not titre or not entreprise or not localisation or not description:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires (*)")
            return
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM utilisateurs WHERE email = %s", (current_user,))
                user_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    INSERT INTO offres_emploi 
                    (recruteur_id, titre, entreprise, localisation, type_contrat, salaire, description, competences)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, titre, entreprise, localisation, type_contrat, salaire, description, competences))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Succès", "Votre offre a été publiée avec succès !")
                show_mes_offres(main_frame)
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la publication: {e}")
>>>>>>> 673ef52ed1871b0b283e6dbaef1fa15e8ae349eb
