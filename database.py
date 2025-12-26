import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from config import DB_CONFIG
from utils import hash_password

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        messagebox.showerror("Erreur BD", f"Erreur de connexion à MySQL: {e}")
        return None

def init_db():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Vérifier si la table existe
        cursor.execute("SHOW TABLES LIKE 'utilisateurs'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("🔄 Migration de la table utilisateurs...")
            
            # Supprimer les anciennes colonnes si elles existent
            cursor.execute("SHOW COLUMNS FROM utilisateurs LIKE 'cherche_travail'")
            if cursor.fetchone():
                try:
                    cursor.execute("ALTER TABLE utilisateurs DROP COLUMN cherche_travail")
                    print("✅ Colonne cherche_travail supprimée")
                except Exception as e:
                    print(f"⚠️ Erreur suppression cherche_travail: {e}")
            
            cursor.execute("SHOW COLUMNS FROM utilisateurs LIKE 'va_postuler'")
            if cursor.fetchone():
                try:
                    cursor.execute("ALTER TABLE utilisateurs DROP COLUMN va_postuler")
                    print("✅ Colonne va_postuler supprimée")
                except Exception as e:
                    print(f"⚠️ Erreur suppression va_postuler: {e}")
            
            # Modifier la colonne type_utilisateur pour inclure 'admin'
            cursor.execute("SHOW COLUMNS FROM utilisateurs LIKE 'type_utilisateur'")
            if cursor.fetchone():
                try:
                    cursor.execute("ALTER TABLE utilisateurs MODIFY COLUMN type_utilisateur ENUM('recruteur', 'chercheur', 'admin') NOT NULL DEFAULT 'chercheur'")
                    print("✅ Colonne type_utilisateur mise à jour avec 'admin'")
                except Exception as e:
                    print(f"⚠️ Erreur modification type_utilisateur: {e}")
            else:
                try:
                    cursor.execute("ALTER TABLE utilisateurs ADD COLUMN type_utilisateur ENUM('recruteur', 'chercheur', 'admin') NOT NULL DEFAULT 'chercheur' AFTER mot_de_passe")
                    print("✅ Colonne type_utilisateur ajoutée")
                except Exception as e:
                    print(f"⚠️ Erreur ajout type_utilisateur: {e}")
        else:
            cursor.execute("""
                CREATE TABLE utilisateurs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    mot_de_passe VARCHAR(255) NOT NULL,
                    type_utilisateur ENUM('recruteur', 'chercheur', 'admin') NOT NULL,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Table utilisateurs créée")
        
        cursor.execute("SELECT * FROM utilisateurs WHERE email = 'admin@jobfinder.ma'")
        if not cursor.fetchone():
            mdp_hash = hash_password("admin123")
            cursor.execute(
                "INSERT INTO utilisateurs (nom, email, mot_de_passe, type_utilisateur) VALUES (%s, %s, %s, %s)",
                ("Administrateur", "admin@jobfinder.ma", mdp_hash, "admin")
            )
            print("✅ Compte administrateur créé (admin@jobfinder.ma / admin123)")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS offres_emploi (
                id INT AUTO_INCREMENT PRIMARY KEY,
                recruteur_id INT NOT NULL,
                titre VARCHAR(200) NOT NULL,
                entreprise VARCHAR(150) NOT NULL,
                localisation VARCHAR(100) NOT NULL,
                type_contrat ENUM('CDI', 'CDD', 'Stage', 'Freelance', 'Alternance') NOT NULL,
                salaire VARCHAR(100),
                description TEXT NOT NULL,
                competences TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recruteur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
            )
        """)
        print("✅ Table offres_emploi créée/vérifiée")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Base de données initialisée avec succès")
    except Error as e:
        print(f"❌ Erreur d'initialisation: {e}")
        messagebox.showerror("Erreur BD", f"Erreur d'initialisation: {e}")