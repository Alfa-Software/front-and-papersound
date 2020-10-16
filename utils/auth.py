def verifica_email(email):  
    usuario, dominio = email.split('@')

    if not len(usuario) >= 1 or not len(dominio) >= 3:
        return False
    elif "@" in usuario or "@" in dominio:
        return False
    elif " " in usuario or " " in dominio:
        return False
    elif not "." in dominio:
        return False
    elif dominio[-1] == ".":
        return False
    else:
        return True
