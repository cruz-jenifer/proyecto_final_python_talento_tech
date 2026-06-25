import sqlite3
import os

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

# INICIO DEL SCRIPT
if __name__ == "__main__":
    # EJECUTA INICIALIZACION
    inicializar_db()
    print("Base de datos inicializada correctamente.")
