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

# INICIO DEL SCRIPT
if __name__ == "__main__":
    # EJECUTA INICIALIZACION
    inicializar_db()
    print("Base de datos inicializada correctamente.")
