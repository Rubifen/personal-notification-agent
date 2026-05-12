import sqlite3
import os

class GestorTareas:
    def __init__(self, db_path="tareas.db"):
        self.db_path = db_path
        self._inicializar_bd()

    def _inicializar_bd(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orden TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'activa',
                recurrencia BOOLEAN NOT NULL DEFAULT 0,
                canal TEXT NOT NULL
            )
        """)
        conexion.commit()
        conexion.close()

    def agregar_tarea(self, orden, canal, recurrencia=False):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO tareas (orden, canal, recurrencia) VALUES (?, ?, ?)",
            (orden, canal, 1 if recurrencia else 0)
        )
        conexion.commit()
        tarea_id = cursor.lastrowid
        conexion.close()
        return tarea_id

    def obtener_tareas(self, estado=None):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        if estado:
            cursor.execute("SELECT id, orden, estado, recurrencia, canal FROM tareas WHERE estado = ?", (estado,))
        else:
            cursor.execute("SELECT id, orden, estado, recurrencia, canal FROM tareas")
        
        filas = cursor.fetchall()
        conexion.close()
        
        tareas = []
        for fila in filas:
            tareas.append({
                "id": fila[0],
                "orden": fila[1],
                "estado": fila[2],
                "recurrencia": bool(fila[3]),
                "canal": fila[4]
            })
        return tareas

    def actualizar_estado(self, tarea_id, estado):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("UPDATE tareas SET estado = ? WHERE id = ?", (estado, tarea_id))
        conexion.commit()
        conexion.close()

    def actualizar_recurrencia(self, tarea_id, recurrencia):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("UPDATE tareas SET recurrencia = ? WHERE id = ?", (1 if recurrencia else 0, tarea_id))
        conexion.commit()
        conexion.close()

    def eliminar_tarea(self, tarea_id):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        conexion.commit()
        conexion.close()
