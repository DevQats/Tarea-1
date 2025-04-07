import sqlite3
import logging
from validaciones import valid_text, valid_descripcion, valid_stock, valid_precio, valid_contraseña, valid_usuario
from getpass import getpass

logging.basicConfig(
    filename='inventario.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    # init schema
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
                 sku INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 descripcion TEXT,
                 cantidad INTEGER NOT NULL,
                 precio REAL NOT NULL,
                 categoria TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                 usuario TEXT PRIMARY KEY,
                 contraseña TEXT NOT NULL)''')
    
    # init user
    c.execute("INSERT OR IGNORE INTO usuarios VALUES ('admin', 'admin')")
    
    conn.commit()
    conn.close()

def auth():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("Usuario: ")
    contraseña = getpass("Contraseña: ")

    c.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", 
              (usuario, contraseña))
    resultado = c.fetchone()

    if resultado is not None:
        logger.info(f'Ha iniciado sesión el usuario {usuario}')
    conn.close()
    return resultado is not None

# -----------------------------------------------------

def add_user():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- REGISTRAR USUARIO ---")
    while True:
        usuario = input("Usuario: ")
        if valid_usuario(usuario):
            break
        else:
            print("Usuario inválido, debe ser alfanumérico con mínimo 3 y máximo 20 caracteres.")

    while True:
        contraseña = getpass("Contraseña: ")
        if valid_contraseña(contraseña):
            break
        else:
            print("Contraseña inválida, debe tener mínimo 6 caracteres.")
    
    c.execute('''INSERT INTO usuarios (usuario, contraseña)
              VALUES (?, ?)''', (usuario, contraseña))
    
    conn.commit()
    conn.close()
    logger.info(f'Se registró el usuario {usuario}')
    print("\nUsuario registrado exitosamente!")

def add_producto():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- AÑADIR PRODUCTO ---")

    while True:
        nombre = input("Nombre del producto: ")
        if valid_text(nombre):
            break
        else:
            print("Nombre inválido, intente nuevamente.")

    while True:
        descripcion = input("Descripción: ")
        if valid_descripcion(descripcion):
            break
        else:
            print("Descripción inválida, intente nuevamente.")
    
    while True:
        cantidad = int(input("Cantidad: "))
        if valid_stock(cantidad):
            break
        else:
            print("Cantidad inválida, intente nuevamente.")

    while True:
        precio = float(input("Precio unitario: "))
        if valid_precio(precio):
            break
        else:
            print("Precio inválido, intente nuevamente.")

    while True:
        categoria = input("Categoría: ")
        if valid_text(categoria):
            break
        else:
            print("Categoría inválida, intente nuevamente.")
    
    c.execute('''INSERT INTO productos 
              (nombre, descripcion, cantidad, precio, categoria)
              VALUES (?, ?, ?, ?, ?)''',
              (nombre, descripcion, cantidad, precio, categoria))
    
    conn.commit()
    conn.close()
    logger.info(f'Se añadió el producto {nombre} con SKU {c.lastrowid}')

def get_productos():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM productos")
    productos = c.fetchall()
    
    print("\n--- PRODUCTOS ---")
    for producto in productos:
        print(f"SKU: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Descripción: {producto[2]}")
        print(f"Cantidad: {producto[3]}")
        print(f"Precio: ${producto[4]}")
        print(f"Categoría: {producto[5]}")
        print("-----------------------")
    
    logger.info(f'Se consultaron los productos')
    conn.close()

def update_producto(sku: int):
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM productos WHERE sku = ?", (sku,))
    producto = c.fetchone()

    print("\n--- ACTUALIZAR PRODUCTO ---")
    if producto:
        while True:
            nombre = input(f"Nuevo nombre (actual: {producto[1]}): ")
            if valid_text(nombre):
                break
            else:
                print("Nombre inválido, intente nuevamente.")

        while True:
            descripcion = input(f"Nueva descripción (actual: {producto[2]}): ")
            if valid_descripcion(descripcion):
                break
            else:
                print("Descripción inválida, intente nuevamente.")

        while True:
            cantidad = int(input(f"Nueva cantidad (actual: {producto[3]}): "))
            if valid_stock(cantidad):
                break
            else:
                print("Cantidad inválida, intente nuevamente.")
         
        while True:
            precio = float(input(f"Nuevo precio (actual: ${producto[4]}): "))
            if valid_precio(precio):
                break
            else:
                print("Precio inválido, intente nuevamente.")
        
        while True:
            categoria = input(f"Nueva categoría (actual: {producto[5]}): ")
            if valid_text(categoria):
                break
            else:
                print("Categoría inválida, intente nuevamente.")

        c.execute('''UPDATE productos SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? 
                  WHERE sku=?''', (nombre, descripcion, cantidad, precio, categoria, sku))
        
        conn.commit()
        logger.info(f'Se actualizó el producto SKU {sku}')
        print("\nProducto actualizado exitosamente!")
    else:
        print("Producto no encontrado.")
    
    conn.close()

def delete_producto(sku: int):
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()

    c.execute("SELECT * FROM productos WHERE sku = ?", (sku,))
    producto = c.fetchone()

    if producto:
        c.execute('''DELETE FROM productos WHERE sku=?''', (sku,))
        
        conn.commit()
        logger.info(f'Se eliminó el producto SKU {sku}')
        print("\nProducto eliminado exitosamente!")
    else:
        print("Producto no encontrado.")
    
    conn.close()

def update_stock(type):
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- ACTUALIZAR STOCK ---")
    sku = int(input("SKU del producto: "))
    
    c.execute("SELECT * FROM productos WHERE sku = ?", (sku,))
    producto = c.fetchone()
    if producto:
        if type == 1:
            cantidad = int(input("Cantidad a ingresar: "))
            c.execute('''UPDATE productos SET cantidad = cantidad + ? WHERE sku = ?''', (cantidad, sku))
            log_msg = f'Se añadieron {cantidad} unidades al producto SKU {sku}'

        elif type == 2:
            cantidad = int(input("Cantidad a vender: "))
            if cantidad <= producto[3]:
                c.execute('''UPDATE productos SET cantidad = cantidad - ? WHERE sku = ?''', (cantidad, sku))
                log_msg = f'Se vendieron {cantidad} unidades del producto SKU {sku}'
            else:
                print(f"\nError: Stock insuficiente. Stock actual: {producto[3]}")
                return

        conn.commit()
    else:
        print("Producto no encontrado.")
    
    conn.close()
    logger.info(log_msg)
    print("\nStock actualizado!")

def lookup_producto():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()

    print("\n--- BUSCAR PRODUCTO ---")
    print("1. Buscar por nombre")
    print("2. Buscar por descripción")
    print("3. Buscar por categoría")

    opcion = int(input("Seleccione una opción: "))
    if opcion == 1:
        nombre = input("Nombre del producto: ")
        c.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    elif opcion == 2:
        descripcion = input("Descripción del producto: ")
        c.execute("SELECT * FROM productos WHERE descripcion LIKE ?", ('%' + descripcion + '%',))
    elif opcion == 3:
        categoria = input("Categoría del producto: ")
        c.execute("SELECT * FROM productos WHERE categoria LIKE ?", ('%' + categoria + '%',))
    else:
        print("Opción inválida.")
        return
    
    productos = c.fetchall()
    if productos:
        print("\n--- PRODUCTOS ENCONTRADOS ---")
        for producto in productos:
            print(f"SKU: {producto[0]}")
            print(f"Nombre: {producto[1]}")
            print(f"Descripción: {producto[2]}")
            print(f"Cantidad: {producto[3]}")
            print(f"Precio: ${producto[4]}")
            print(f"Categoría: {producto[5]}")
            print("-----------------------")
    else:
        print("No se encontraron productos.")

def gen_report():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- REPORTE ---")
    c.execute("SELECT sum(cantidad) FROM productos")
    cantidad = c.fetchall()
    if cantidad:
        print(f"{cantidad[0][0]} productos en inventario")
    
    c.execute("SELECT sum(cantidad * precio) FROM productos")
    precio_total = c.fetchall()
    if precio_total:
        print(f"Valor total del inventario: ${precio_total[0][0]}")

    c.execute("SELECT * FROM productos where cantidad = 0")
    out_stock = c.fetchall()
    if out_stock:
        print("\nProductos sin stock:")
        for producto in out_stock:
            print(f"SKU: {producto[0]}")
            print(f"Nombre: {producto[1]}")
            print(f"Descripción: {producto[2]}")
            print(f"Cantidad: {producto[3]}")
            print(f"Precio: ${producto[4]}")
            print(f"Categoría: {producto[5]}")
            print("-----------------------")
    conn.close()

    logger.info('Se generó un reporte de productos')
    print("\nReporte generado exitosamente!")