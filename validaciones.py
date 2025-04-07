import re
import logging

def valid_text(text):
    return re.match("^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]+$", text)

def valid_descripcion(text):
    return re.match("^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,;: ]+$", text)

def valid_stock(stock):
    if isinstance(stock, int) and stock > 0:
        return True
    elif isinstance(stock, int) and stock == 0:
        logging.warning("Esta ingresando un nuevo producto sin stock.")
        return True
    else:
        return False

def valid_precio(precio):
    if isinstance(precio, (int, float)) and precio >= 0:
        return True
    else:
        return False

def valid_usuario(usuario):
    return re.match(r"^[a-zA-Z0-9_.]{3,20}$", usuario)

def valid_contraseña(contraseña):
    if len(contraseña) < 6:
        return False
    return True
