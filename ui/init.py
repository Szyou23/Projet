
"""
Module UI pour JobFinder
"""

# Variables globales partagées entre les modules UI
current_user = None
user_type = None
btnEtat = False

def set_current_user(email, u_type):
    
    global current_user, user_type
    current_user = email
    user_type = u_type

def get_current_user():
    
    return current_user, user_type

def logout_user():
    
    global current_user, user_type
    current_user = None
    user_type = None

def toggle_btn_state():
    
    global btnEtat
    btnEtat = not btnEtat
    return btnEtat

def get_btn_state():
    
    return btnEtat

def set_btn_state(state):
    
    global btnEtat
    btnEtat = state