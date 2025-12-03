"""
Fonctions utilitaires pour JobFinder
"""
import hashlib
import re

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def valider_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False
    
    # Vérifications supplémentaires
    if email.count('@') != 1:
        return False
    
    # Vérifier la longueur minimale
    if len(email) < 5:
        return False
    
    return True