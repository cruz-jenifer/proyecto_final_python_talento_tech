import sqlite3
import os
import sys
from colorama import init, Fore, Style

# INICIALIZAMOS COLORAMA Y FORZAMOS UTF8 PARA EVITAR ERRORES CON EMOJIS
sys.stdout.reconfigure(encoding='utf-8')
init(autoreset=True)

# CONFIGURACION DE LA BASE DE DATOS

def conectar_db():
    # CONECTA CON LA BASE DE DATOS
    try:
        conexion = sqlite3.connect('inventario.db')
        return conexion
    except sqlite3.Error as e:
        # CAPTURA ERROR DE CONEXION
        print(f"Error al conectar con la base de datos: {e}")
        return None

def inicializar_db():
    # INICIALIZA LA BASE DE DATOS
    conexion = conectar_db()
    if conexion is not None:
        try:
            # CREA EL CURSOR
            cursor = conexion.cursor()
            
            # CREA LA TABLA PRODUCTOS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            ''')
            
            # GUARDA LOS CAMBIOS
            conexion.commit()
            
        except sqlite3.Error as e:
            print(f"Error al crear la tabla 'productos': {e}")
            
        finally:
            # CIERRA CURSOR Y CONEXION
            if cursor:
                cursor.close()
            conexion.close()
# LOGICA DE NEGOCIO Y OPERACIONES CRUD

def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    # REGISTRA UN NUEVO PRODUCTO EN LA BASE DE DATOS
    # UTILIZA CONSULTAS PARAMETRIZADAS PARA PREVENIR INYECCION SQL
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            # LA TUPLA DE VALORES SE PASA AL METODO EXECUTE
            consulta = '''
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            '''
            cursor.execute(consulta, (nombre, descripcion, cantidad, precio, categoria))
            conexion.commit()
            print("\n✅ Producto registrado con éxito.")
        except sqlite3.Error as e:
            print(f"\n❌ Error al registrar el producto: {e}")
        finally:
            cursor.close()
            conexion.close()

def visualizar_productos():
    # RECUPERA Y MUESTRA TODOS LOS PRODUCTOS REGISTRADOS EN LA TABLA
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos")
            # DEVUELVE UNA LISTA CON TODAS LAS TUPLAS RESULTANTES
            productos = cursor.fetchall()
            
            if productos:
                print("\n--- LISTADO DE PRODUCTOS ---")
                for prod in productos:
                    print(f"ID: {prod[0]} | Nombre: {prod[1]} | Desc: {prod[2]} | Cant: {prod[3]} | Precio: ${prod[4]:.2f} | Cat: {prod[5]}")
            else:
                print("\n⚠️ No hay productos registrados en el inventario.")
        except sqlite3.Error as e:
            print(f"\n❌ Error al recuperar los productos: {e}")
        finally:
            cursor.close()
            conexion.close()

def buscar_producto(id_producto):
    # BUSCA UN PRODUCTO ESPECIFICO MEDIANTE SU ID
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
            # DEVUELVE UNA UNICA TUPLA O NINGUNA SI NO HAY COINCIDENCIAS
            producto = cursor.fetchone()
            
            if producto:
                print("\n--- PRODUCTO ENCONTRADO ---")
                print(f"ID: {producto[0]} | Nombre: {producto[1]} | Desc: {producto[2]} | Cant: {producto[3]} | Precio: ${producto[4]:.2f} | Cat: {producto[5]}")
                return producto
            else:
                print(f"\n⚠️ No se encontró ningún producto con el ID {id_producto}.")
                return None
        except sqlite3.Error as e:
            print(f"\n❌ Error al buscar el producto: {e}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_producto(id_producto, nueva_cantidad, nuevo_precio):
    # ACTUALIZA LA CANTIDAD O EL PRECIO DE UN PRODUCTO EXISTENTE MEDIANTE SU ID
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = '''
                UPDATE productos 
                SET cantidad = ?, precio = ? 
                WHERE id = ?
            '''
            cursor.execute(consulta, (nueva_cantidad, nuevo_precio, id_producto))
            
            # NOS INDICA CUANTAS FILAS FUERON AFECTADAS POR EL UPDATE
            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\n✅ Producto ID {id_producto} actualizado correctamente.")
            else:
                print(f"\n⚠️ No se encontró el producto con ID {id_producto}. No se realizaron cambios.")
        except sqlite3.Error as e:
            print(f"\n❌ Error al actualizar el producto: {e}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_producto(id_producto):
    # ELIMINA UN PRODUCTO DE LA BASE DE DATOS MEDIANTE SU ID
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            
            if cursor.rowcount > 0:
                conexion.commit()
                print(f"\n✅ Producto ID {id_producto} eliminado exitosamente.")
            else:
                print(f"\n⚠️ No se encontró el producto con ID {id_producto}.")
        except sqlite3.Error as e:
            print(f"\n❌ Error al eliminar el producto: {e}")
        finally:
            cursor.close()
            conexion.close()

def reporte_bajo_stock(limite):
    # MUESTRA LOS PRODUCTOS CUYA CANTIDAD DISPONIBLE ES IGUAL O INFERIOR AL LIMITE ESPECIFICADO
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
            productos = cursor.fetchall()
            
            if productos:
                print(f"\n--- REPORTE DE BAJO STOCK (Límite: {limite}) ---")
                for prod in productos:
                    print(f"ID: {prod[0]} | Nombre: {prod[1]} | Cantidad actual: {prod[3]}")
            else:
                print(f"\n✅ Todos los productos tienen un stock superior a {limite}.")
        except sqlite3.Error as e:
            print(f"\n❌ Error al generar el reporte: {e}")
        finally:
            cursor.close()
            conexion.close()

# INTERFAZ DE USUARIO Y MENU PRINCIPAL

def mostrar_menu():
    # IMPRIME EL MENU PRINCIPAL EN LA CONSOLA CON COLORES
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*45)
    print(Fore.CYAN + Style.BRIGHT + "   📦 SISTEMA DE GESTIÓN DE INVENTARIO   ")
    print(Fore.CYAN + Style.BRIGHT + "="*45)
    print(Fore.YELLOW + "1. Registrar nuevo producto")
    print(Fore.YELLOW + "2. Visualizar todos los productos")
    print(Fore.YELLOW + "3. Buscar producto por ID")
    print(Fore.YELLOW + "4. Actualizar datos de producto (Cantidad/Precio)")
    print(Fore.YELLOW + "5. Eliminar producto")
    print(Fore.YELLOW + "6. Reporte de bajo stock")
    print(Fore.RED + "7. Salir")
    print(Fore.CYAN + "="*45)

def menu_principal():
    # CONTROLADOR PRINCIPAL DEL PROGRAMA
    # ASEGURAMOS QUE LA BASE DE DATOS Y LA TABLA EXISTAN ANTES DE EMPEZAR
    inicializar_db()
    
    # BUCLE INFINITO QUE MANTIENE EL PROGRAMA ABIERTO
    while True:
        mostrar_menu()
        opcion = input(Fore.GREEN + Style.BRIGHT + "Seleccione una opción (1-7): ")
        
        if opcion == '1':
            print(Fore.MAGENTA + "\n--- REGISTRAR PRODUCTO ---")
            try:
                nombre = input("Nombre del producto: ")
                descripcion = input("Descripción: ")
                # VALIDAMOS QUE LA CANTIDAD SEA UN ENTERO Y EL PRECIO UN NUMERO REAL
                cantidad = int(input("Cantidad disponible: "))
                precio = float(input("Precio: $"))
                categoria = input("Categoría: ")
                
                registrar_producto(nombre, descripcion, cantidad, precio, categoria)
            except ValueError:
                # EVITA QUE EL PROGRAMA SE CIERRE POR UN ERROR DE TIPEO
                print(Fore.RED + "❌ Error: Ingrese un número entero para la cantidad y un valor numérico para el precio.")

        elif opcion == '2':
            visualizar_productos()

        elif opcion == '3':
            print(Fore.MAGENTA + "\n--- BUSCAR PRODUCTO ---")
            try:
                id_prod = int(input("Ingrese el ID del producto: "))
                buscar_producto(id_prod)
            except ValueError:
                print(Fore.RED + "❌ Error: El ID debe ser un número entero.")

        elif opcion == '4':
            print(Fore.MAGENTA + "\n--- ACTUALIZAR PRODUCTO ---")
            try:
                id_prod = int(input("Ingrese el ID del producto a modificar: "))
                nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
                nuevo_precio = float(input("Ingrese el nuevo precio: $"))
                actualizar_producto(id_prod, nueva_cantidad, nuevo_precio)
            except ValueError:
                print(Fore.RED + "❌ Error: Datos inválidos. Verifique que el ID y la cantidad sean enteros, y el precio numérico.")

        elif opcion == '5':
            print(Fore.MAGENTA + "\n--- ELIMINAR PRODUCTO ---")
            try:
                id_prod = int(input("Ingrese el ID del producto a eliminar: "))
                # PEDIMOS CONFIRMACION ANTES DE ELIMINAR
                confirmacion = input(Fore.RED + f"¿Está seguro que desea eliminar el ID {id_prod}? (s/n): ").lower()
                if confirmacion == 's':
                    eliminar_producto(id_prod)
                else:
                    print("Operación cancelada.")
            except ValueError:
                print(Fore.RED + "❌ Error: El ID debe ser un número entero.")

        elif opcion == '6':
            print(Fore.MAGENTA + "\n--- REPORTE DE BAJO STOCK ---")
            try:
                limite = int(input("Ingrese el límite mínimo de stock para el reporte: "))
                reporte_bajo_stock(limite)
            except ValueError:
                print(Fore.RED + "❌ Error: El límite debe ser un número entero.")

        elif opcion == '7':
            print(Fore.GREEN + Style.BRIGHT + "\n¡Gracias por utilizar el Sistema de Gestión de Inventario! Hasta luego.\n")
            # TERMINA EL BUCLE Y FINALIZA LA EJECUCION
            break
            
        else:
            print(Fore.RED + "❌ Opción no válida. Por favor, intente nuevamente eligiendo un número del 1 al 7.")

# PUNTO DE ENTRADA DEL SCRIPT
if __name__ == "__main__":
    menu_principal()
