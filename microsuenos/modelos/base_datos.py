import sqlite3
from datetime import datetime

class BaseDatos:
    def __init__(self):
        self.conn = sqlite3.connect("microsuenos.db")
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        # Crear tabla para almacenar los resultados de los análisis
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            estado TEXT,
            detalles TEXT
        )
        """)
        self.conn.commit()

    def guardar_resultado(self, estado, detalles):
        # Guardar un resultado en la base de datos
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO resultados (fecha, estado, detalles) VALUES (?, ?, ?)", (fecha, estado, detalles))
        self.conn.commit()

    def obtener_resultados(self):
        # Obtener todos los resultados de la base de datos
        self.cursor.execute("SELECT * FROM resultados")
        return self.cursor.fetchall()

    def cerrar(self):
        self.conn.close()
