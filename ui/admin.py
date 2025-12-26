import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from config import COULEURS
from database import get_db_connection
import ui

def show_admin_dashboard(main_frame, go_users_callback, go_offres_callback):
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    headerFrame = tk.Frame(main_frame, bg=COULEURS["admin"], height=150)
    headerFrame.pack(fill="x")
    
    tk.Label(
        headerFrame,
        text="⚙️ Tableau de bord Administrateur",
        font=("Arial", 24, "bold"),
        bg=COULEURS["admin"],
        fg=COULEURS["white"]
    ).pack(pady=50)
    
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

def show_admin_utilisateurs(main_frame):
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
    
    headerFrame = tk.Frame(scrollableFrame, bg=COULEURS["admin"], height=100)
    headerFrame.pack(fill="x")
    
    tk.Label(
        headerFrame,
        text="👥 Gestion des utilisateurs",
        font=("Arial", 22, "bold"),
        bg=COULEURS["admin"],
        fg=COULEURS["white"]
    ).pack(pady=30)
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nom, email, type_utilisateur, date_creation
                FROM utilisateurs
                WHERE type_utilisateur != 'admin'
                ORDER BY date_creation DESC
            """)
            utilisateurs = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if utilisateurs:
                for user in utilisateurs:
                    user_id, nom, email, type_user, date_creation = user
                    
                    cardFrame = tk.Frame(scrollableFrame, bg=COULEURS["white"], bd=2, relief="groove")
                    cardFrame.pack(pady=10, padx=30, fill="x")
                    
                    tk.Label(
                        cardFrame,
                        text=nom,
                        font=("Arial", 14, "bold"),
                        bg=COULEURS["white"],
                        fg=COULEURS["primary"]
                    ).pack(anchor="w", padx=20, pady=(15, 5))
                    
                    tk.Label(
                        cardFrame,
                        text=f"✉️ {email}",
                        font=("Arial", 11),
                        bg=COULEURS["white"],
                        fg=COULEURS["dark"]
                    ).pack(anchor="w", padx=20)
                    
                    type_display = "💼 Recruteur" if type_user == "recruteur" else "🔍 Chercheur d'emploi"
                    type_color = COULEURS["warning"] if type_user == "recruteur" else COULEURS["success"]
                    
                    tk.Label(
                        cardFrame,
                        text=type_display,
                        font=("Arial", 10, "bold"),
                        bg=COULEURS["white"],
                        fg=type_color
                    ).pack(anchor="w", padx=20, pady=5)
                    
                    tk.Label(
                        cardFrame,
                        text=f"Inscrit le {date_creation.strftime('%d/%m/%Y')}",
                        font=("Arial", 9),
                        bg=COULEURS["white"],
                        fg="gray"
                    ).pack(anchor="w", padx=20, pady=(0, 10))
                    
                    tk.Button(
                        cardFrame,
                        text="🗑️ Supprimer l'utilisateur",
                        font=("Arial", 9, "bold"),
                        bg=COULEURS["danger"],
                        fg=COULEURS["white"],
                        cursor="hand2",
                        bd=0,
                        width=25,
                        command=lambda uid=user_id, unom=nom: supprimer_utilisateur(main_frame, uid, unom)
                    ).pack(pady=10)
            else:
                tk.Label(
                    scrollableFrame,
                    text="Aucun utilisateur inscrit",
                    font=("Arial", 13),
                    bg=COULEURS["light_bg"],
                    fg=COULEURS["dark"]
                ).pack(pady=50)
                
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def supprimer_utilisateur(main_frame, user_id, nom):
    reponse = messagebox.askyesno(
        "Confirmation",
        f"Êtes-vous sûr de vouloir supprimer l'utilisateur '{nom}' ?\nToutes ses offres seront également supprimées."
    )
    
    if reponse:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM utilisateurs WHERE id = %s", (user_id,))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Succès", "L'utilisateur a été supprimé avec succès !")
                show_admin_utilisateurs(main_frame)
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")

def show_admin_offres(main_frame):
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
    
    headerFrame = tk.Frame(scrollableFrame, bg=COULEURS["admin"], height=100)
    headerFrame.pack(fill="x")
    
    tk.Label(
        headerFrame,
        text="💼 Gestion des offres d'emploi",
        font=("Arial", 22, "bold"),
        bg=COULEURS["admin"],
        fg=COULEURS["white"]
    ).pack(pady=30)
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id, o.titre, o.entreprise, o.localisation, o.type_contrat, 
                       o.salaire, o.date_creation, u.nom
                FROM offres_emploi o
                JOIN utilisateurs u ON o.recruteur_id = u.id
                ORDER BY o.date_creation DESC
            """)
            offres = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if offres:
                for offre in offres:
                    offre_id, titre, entreprise, localisation, type_contrat, salaire, date_creation, recruteur = offre
                    
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
                        text=f"Publiée le {date_creation.strftime('%d/%m/%Y')} par {recruteur}",
                        font=("Arial", 9),
                        bg=COULEURS["white"],
                        fg="gray"
                    ).pack(anchor="w", padx=20, pady=(0, 10))
                    
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
                        width=15,
                        command=lambda oid=offre_id: voir_offre_admin(main_frame, oid)
                    ).pack(side="left", padx=5)
                    
                    tk.Button(
                        btnActionFrame,
                        text="🗑️ Supprimer",
                        font=("Arial", 9, "bold"),
                        bg=COULEURS["danger"],
                        fg=COULEURS["white"],
                        cursor="hand2",
                        bd=0,
                        width=15,
                        command=lambda oid=offre_id: supprimer_offre_admin(main_frame, oid)
                    ).pack(side="left", padx=5)
            else:
                tk.Label(
                    scrollableFrame,
                    text="Aucune offre d'emploi disponible",
                    font=("Arial", 13),
                    bg=COULEURS["light_bg"],
                    fg=COULEURS["dark"]
                ).pack(pady=50)
                
        except Error as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def voir_offre_admin(main_frame, offre_id):
    from ui.offers import voir_offre
    voir_offre(main_frame, offre_id)

def supprimer_offre_admin(main_frame, offre_id):
    from ui.offers import supprimer_offre
    supprimer_offre(main_frame, offre_id)