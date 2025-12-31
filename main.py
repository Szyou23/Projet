import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from config import COULEURS, APP_CONFIG, IMAGES
from database import init_db
import ui
from ui.auth import show_inscription, show_connexion
from ui.profile import show_profil
from ui.contact import show_contact
from ui.offers import show_offres
from ui.admin import show_admin_dashboard
from ui.settings import show_parametres

class JobFinderApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title(APP_CONFIG['title'])
        self.app.config(bg=COULEURS["light_bg"])
        self.app.geometry(APP_CONFIG['geometry'])
        self.app.resizable(APP_CONFIG['resizable'], APP_CONFIG['resizable'])
        
        try:
            self.app.iconbitmap(IMAGES['logo'])
        except:
            pass
        
        # Chargement des images
        self.load_images()
        
        # Création de l'interface
        self.create_ui()
        
        # Initialisation de la base de données
        self.init_database()
        
        # Affichage de la page d'accueil
        self.show_accueil()
    
    def load_images(self):
        
        try:
            self.navIcon = ImageTk.PhotoImage(Image.open(IMAGES['menu']).resize((25, 25)))
            self.closeIcon = ImageTk.PhotoImage(Image.open(IMAGES['close']).resize((25, 25)))
        except:
            self.navIcon = self.closeIcon = None
    
    def create_ui(self):
        
        # Barre du haut
        self.topFrame = tk.Frame(self.app, bg=COULEURS["primary"], height=60)
        self.topFrame.pack(side="top", fill=tk.X)
        
        self.navbarBtn = tk.Button(
            self.topFrame,
            image=self.navIcon,
            bg=COULEURS["primary"],
            bd=0,
            padx=20,
            activebackground=COULEURS["primary_dark"],
            cursor="hand2",
            command=self.toggle_menu
        )
        self.navbarBtn.place(x=10, y=15)
        
        accueilText = tk.Label(
            self.topFrame,
            text="JobFinder",
            font=("Arial", 18, "bold"),
            bg=COULEURS["primary"],
            fg=COULEURS["white"],
            height=2,
            padx=20
        )
        accueilText.pack(side="right")
        
        # Contenu principal
        self.mainFrame = tk.Frame(self.app, bg=COULEURS["light_bg"])
        self.mainFrame.pack(fill="both", expand=True)
        
        # Menu latéral
        self.create_sidebar()
    
    def create_sidebar(self):
        
        self.navLateral = tk.Frame(self.app, bg="#263238", width=300, height=700)
        self.navLateral.place(x=-300, y=0)
        
        tk.Label(
            self.navLateral,
            text="MENU",
            font=("Arial", 16, "bold"),
            bg=COULEURS["primary"],
            fg=COULEURS["white"],
            width=300,
            height=2
        ).place(x=0, y=0)
        
        self.update_menu()

    def update_menu(self):
        
        current_user, user_type = ui.get_current_user()
        
        if user_type == "admin":
            menu_buttons = [
                ("🏠  Accueil", self.show_accueil),
                ("📊  Dashboard Admin", self.go_admin_dashboard),
                ("👥  Utilisateurs", lambda: self.go_admin_users()),
                ("💼  Offres d'emploi", self.go_offres),
                ("⚙️  Paramètres", self.go_parametres),
                ("📞  Contact", self.go_contact)
            ]
        else:
            menu_buttons = [
                ("🏠  Accueil", self.show_accueil),
                ("👤  Profil", self.go_profil),
                ("💼  Offres d'emploi", self.go_offres),
                ("⚙️  Paramètres", self.go_parametres),
                ("📞  Contact", self.go_contact)
            ]
        
        # Effacer les anciens boutons
        for widget in self.navLateral.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        y = 80
        for text, cmd in menu_buttons:
            btn = tk.Button(
                self.navLateral,
                text=text,
                font=("Arial", 13, "bold"),
                bg="#263238",
                fg=COULEURS["white"],
                activebackground="#37474f",
                bd=0,
                cursor="hand2",
                anchor="w",
                padx=20,
                width=25,
                height=2,
                command=cmd
            )
            btn.place(x=0, y=y)
            
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#37474f"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#263238"))
            
            y += 55
    
    def toggle_menu(self):
        """Toggle l'animation du menu"""
        if ui.get_btn_state():
            for x in range(0, 301, 15):
                self.navLateral.place(x=-x, y=0)
                self.app.update()
            self.navLateral.place(x=-300, y=0)
            self.navbarBtn.config(image=self.navIcon)
            ui.set_btn_state(False)
        else:
            self.update_menu()
            for x in range(-300, 1, 15):
                self.navLateral.place(x=x, y=0)
                self.app.update()
            self.navLateral.place(x=0, y=0)
            self.topFrame.tkraise()
            self.navbarBtn.config(image=self.closeIcon)
            ui.set_btn_state(True)
    
    def close_menu_if_open(self):
        """Ferme le menu s'il est ouvert"""
        if ui.get_btn_state():
            self.toggle_menu()
    
    def show_accueil(self):
        """Affiche la page d'accueil"""
        self.close_menu_if_open()
        
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        heroFrame = tk.Frame(self.mainFrame, bg=COULEURS["primary"], height=300)
        heroFrame.pack(fill="x")

        tk.Label(
            heroFrame,
            text="Trouvez l'emploi de vos rêves",
            font=("Arial", 28, "bold"),
            bg=COULEURS["primary"],
            fg=COULEURS["white"],
            wraplength=500
        ).pack(pady=(50, 10))

        tk.Label(
            heroFrame,
            text="Connectez-vous avec les meilleures entreprises\net construisez la carrière que vous méritez",
            font=("Arial", 13),
            bg=COULEURS["primary"],
            fg=COULEURS["white"],
            wraplength=500,
            justify="center"
        ).pack(pady=(0, 40))

        buttonsFrame = tk.Frame(self.mainFrame, bg=COULEURS["light_bg"])
        buttonsFrame.pack(fill="both", expand=True)

        current_user, user_type = ui.get_current_user()
        
        if current_user:
            btnContainer = tk.Frame(buttonsFrame, bg=COULEURS["light_bg"])
            btnContainer.place(relx=0.5, rely=0.3, anchor="center")
            
            from database import get_db_connection
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT nom FROM utilisateurs WHERE email = %s", (current_user,))
                    user = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    
                    if user:
                        nom = user[0]
                        tk.Label(
                            btnContainer,
                            text=f"Bienvenue, {nom} ! 👋",
                            font=("Arial", 20, "bold"),
                            bg=COULEURS["light_bg"],
                            fg=COULEURS["primary"]
                        ).pack(pady=20)
                except:
                    pass
            
            # Affichage différent pour l'admin
            if user_type == "admin":
                tk.Button(
                    btnContainer,
                    text="📊 Tableau de bord Admin",
                    font=("Arial", 14, "bold"),
                    bg=COULEURS["admin"],
                    fg=COULEURS["white"],
                    width=25,
                    height=2,
                    cursor="hand2",
                    bd=0,
                    command=self.go_admin_dashboard
                ).pack(pady=15)
            else:
                tk.Button(
                    btnContainer,
                    text="Voir mon profil",
                    font=("Arial", 14, "bold"),
                    bg=COULEURS["primary"],
                    fg=COULEURS["white"],
                    width=25,
                    height=2,
                    cursor="hand2",
                    bd=0,
                    command=self.go_profil
                ).pack(pady=15)
            
            tk.Button(
                btnContainer,
                text="Voir les offres d'emploi",
                font=("Arial", 14, "bold"),
                bg=COULEURS["success"],
                fg=COULEURS["white"],
                width=25,
                height=2,
                cursor="hand2",
                bd=0,
                command=self.go_offres
            ).pack(pady=15)
        else:
            btnContainer = tk.Frame(buttonsFrame, bg=COULEURS["light_bg"])
            btnContainer.place(relx=0.5, rely=0.3, anchor="center")

            tk.Button(
                btnContainer,
                text="Se connecter",
                font=("Arial", 14, "bold"),
                bg=COULEURS["primary"],
                fg=COULEURS["white"],
                width=25,
                height=2,
                cursor="hand2",
                bd=0,
                command=self.go_connexion
            ).pack(pady=15)

            tk.Button(
                btnContainer,
                text="Créer un compte",
                font=("Arial", 14, "bold"),
                bg=COULEURS["white"],
                fg=COULEURS["primary"],
                width=25,
                height=2,
                cursor="hand2",
                bd=2,
                relief="solid",
                command=self.go_inscription
            ).pack(pady=15)
    
    def go_inscription(self):
        """Affiche la page d'inscription"""
        self.close_menu_if_open()
        show_inscription(self.mainFrame, self.go_profil, self.go_connexion)
    
    def go_connexion(self):
        """Affiche la page de connexion"""
        self.close_menu_if_open()
        show_connexion(self.mainFrame, self.go_profil, self.go_admin_dashboard, self.go_inscription)
    
    def go_profil(self):
        """Affiche le profil"""
        self.close_menu_if_open()
        show_profil(self.mainFrame, self.go_connexion, self.go_inscription, self.show_accueil)
    
    def go_contact(self):
        """Affiche la page contact"""
        self.close_menu_if_open()
        show_contact(self.mainFrame)
    
    def go_offres(self):
        """Affiche les offres"""
        self.close_menu_if_open()
        show_offres(self.mainFrame, self.go_connexion)
    
    def go_admin_dashboard(self):
        """Affiche le dashboard admin"""
        self.close_menu_if_open()
        show_admin_dashboard(self.mainFrame, lambda: self.go_admin_users(), lambda: self.go_offres())
    
    def go_admin_users(self):
        """Affiche la gestion des utilisateurs (admin)"""
        from ui.admin import show_admin_utilisateurs
        self.close_menu_if_open()
        show_admin_utilisateurs(self.mainFrame)
    
    def go_parametres(self):
        """Affiche les paramètres"""
        self.close_menu_if_open()
        show_parametres(self.mainFrame, self.go_connexion, self.show_accueil)
    
    def init_database(self):
        """Initialise la base de données"""
        try:
            init_db()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'initialisation: {e}")
            self.app.destroy()
    
    def run(self):
        """Lance l'application"""
        self.app.mainloop()

if __name__ == "__main__":
    app = JobFinderApp()
    app.run()