class Registro:
    def __init__(self, db):
        self.db = db

    def agregar_conductor(self, nombre, edad, experiencia):
        self.db.cursor.execute('''
        INSERT INTO conductores (nombre, edad, experiencia)
        VALUES (?, ?, ?)
        ''', (nombre, edad, experiencia))
        self.db.conexion.commit()
