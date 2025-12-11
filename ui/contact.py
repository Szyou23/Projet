"""
Page de contact
"""
import tkinter as tk
import webbrowser
from config import COULEURS


def show_contact(main_frame):
    """Affiche la page de contact"""
    for widget in main_frame.winfo_children():
        widget.destroy()

    container = tk.Frame(main_frame, bg=COULEURS["white"], width=500, height=550)
    container.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        container,
        text="Contactez-nous",
        font=("Arial", 24, "bold"),
        bg=COULEURS["white"],
        fg=COULEURS["primary"]
    ).pack(pady=30)

    tk.Label(
        container,
        text="Notre équipe est là pour vous aider",
        font=("Arial", 11),
        bg=COULEURS["white"],
        fg=COULEURS["dark"]
    ).pack(pady=(0, 30))

    contact_info = [
        ("📞", "Téléphone", "+212 612 345 678", "tel:+212612345678"),
        ("✉️", "Email", "contact@jobfinder.ma", "mailto:contact@jobfinder.ma"),
        ("📍", "Adresse", "Oujda, Maroc", None),
        ("🌐", "Site web", "www.jobfinder.ma", "https://www.jobfinder.ma")
    ]

    for icon, titre, valeur, lien in contact_info:
        frame = tk.Frame(container, bg=COULEURS["white"])
        frame.pack(pady=10, padx=40, fill="x")
        
        tk.Label(frame, text=icon, font=("Arial", 16), bg=COULEURS["white"]).pack(side="left", padx=10)
        
        infoFrame = tk.Frame(frame, bg=COULEURS["white"])
        infoFrame.pack(side="left", fill="x", expand=True)
        
        tk.Label(infoFrame, text=titre, font=("Arial", 10, "bold"),
                bg=COULEURS["white"], fg=COULEURS["dark"], anchor="w").pack(anchor="w")
        
        label = tk.Label(
            infoFrame,
            text=valeur,
            font=("Arial", 11),
            bg=COULEURS["white"],
            fg=COULEURS["primary"] if lien else COULEURS["dark"],
            anchor="w",
            cursor="hand2" if lien else "arrow"
        )
        label.pack(anchor="w")
        
        if lien:
            label.bind("<Button-1>", lambda e, url=lien: webbrowser.open(url))
            label.bind("<Enter>", lambda e, l=label: l.config(font=("Arial", 11, "underline")))
            label.bind("<Leave>", lambda e, l=label: l.config(font=("Arial", 11)))