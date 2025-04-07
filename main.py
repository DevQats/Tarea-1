import logging
from func import add_user, add_producto, get_productos, update_stock, init_db, auth, update_producto, delete_producto, lookup_producto, gen_report

def menu():
    while True:
        print("\n----------------------\n")
        print("1. Registrar usuario")
        print("2. Agregar producto")
        print("3. Ver todos los productos")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Actualizar stock")
        print("7. Buscar productos")
        print("8. Generar reporte")
        print("9. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            add_user()
        elif opcion == '2':
            add_producto()
        elif opcion == '3':
            get_productos()
        elif opcion == '4':
            sku = int(input("SKU del producto a actualizar: "))
            update_producto(sku)
        elif opcion == '5':
            sku = int(input("SKU del producto a eliminar: "))
            delete_producto(sku)
        elif opcion == '6':
            print("\n-------------------")
            print("1. Ingresar stock")
            print("2. Vender stock")

            opcion = input("\nSeleccione una opción: ")
            if opcion == '1' or opcion == '2':
                update_stock(int(opcion))
            else:
                print("Opción inválida, intente nuevamente.")
                continue
        elif opcion == '7':
            lookup_producto()
        elif opcion == '8':
            gen_report()
        elif opcion == '9':
            break
        else:
            print("Opción inválida, intente nuevamente.")

if __name__ == "__main__":
    logging.basicConfig(filename='inventario.log', level=logging.INFO)
    init_db()
    
    if auth():
        menu()
    else:
        print("\nUsuario o contraseña incorrectos.")