from flask_login import  current_user

def get_greeting():
    return f"Welcome {current_user.username}" if current_user.is_authenticated else "Afrolodge your home"