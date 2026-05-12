import sqlite3
import os
import datetime

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
                intencion_json TEXT,
                estado TEXT NOT NULL DEFAULT 'activa',
                recurrencia BOOLEAN NOT NULL DEFAULT 0,
                canal TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL,
                ultima_ejecucion TEXT,
                frecuencia_minutos INTEGER NOT NULL DEFAULT 1
            )
        """)
        conexion.commit()
        conexion.close()

    def agregar_tarea(self, orden, canal, intencion_json, frecuencia_minutos, recurrencia=False):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        fecha_creacion = datetime.datetime.now().isoformat()
        cursor.execute(
            """INSERT INTO tareas 
            (orden, canal, intencion_json, frecuencia_minutos, recurrencia, fecha_creacion) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (orden, canal, intencion_json, frecuencia_minutos, 1 if recurrencia else 0, fecha_creacion)
        )
        conexion.commit()
        tarea_id = cursor.lastrowid
        conexion.close()
        return tarea_id

    def obtener_tareas(self, estado=None):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        if estado:
            cursor.execute("SELECT id, orden, estado, recurrencia, canal, intencion_json, fecha_creacion, ultima_ejecucion, frecuencia_minutos FROM tareas WHERE estado = ?", (estado,))
        else:
            cursor.execute("SELECT id, orden, estado, recurrencia, canal, intencion_json, fecha_creacion, ultima_ejecucion, frecuencia_minutos FROM tareas")
        
        filas = cursor.fetchall()
        conexion.close()
        
        tareas = []
        for fila in filas:
            tareas.append({
                "id": fila[0],
                "orden": fila[1],
                "estado": fila[2],
                "recurrencia": bool(fila[3]),
                "canal": fila[4],
                "intencion_json": fila[5],
                "fecha_creacion": fila[6],
                "ultima_ejecucion": fila[7],
                "frecuencia_minutos": fila[8]
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

    def actualizar_ultima_ejecucion(self, tarea_id):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        ahora = datetime.datetime.now().isoformat()
        cursor.execute("UPDATE tareas SET ultima_ejecucion = ? WHERE id = ?", (ahora, tarea_id))
        conexion.commit()
        conexion.close()

    def eliminar_tarea(self, tarea_id):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        conexion.commit()
        conexion.close()
