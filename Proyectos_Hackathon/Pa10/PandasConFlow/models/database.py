"""
Gestión de base de datos para PiLearn
"""

import sqlite3
import os
from .exercise import Exercise
from .lesson import Lesson


class Database:
    """Clase para gestionar la base de datos de PiLearn"""
    
    def __init__(self, db_path="pitutor_raspberry.db"):
        self.db_path = db_path
        self.conn = None
    
    def conectar(self):
        """Establecer conexión con la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=NORMAL")
            self.conn.execute("PRAGMA cache_size=1000")
            return True
        except Exception as e:
            print(f"❌ Error conectando a BD: {e}")
            return False
    
    def desconectar(self):
        """Cerrar conexión con la base de datos"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def inicializar(self):
        """Inicializar base de datos con tablas y datos iniciales"""
        if not self.conectar():
            return False, "Error de conexión"
        
        try:
            c = self.conn.cursor()
            
            c.execute("PRAGMA table_info(ejercicios)")
            columns = c.fetchall()
            column_names = [col[1] for col in columns]
            
            needs_migration = not columns or 'materia' not in column_names
            
            if needs_migration:
                print("⚙ Migrando base de datos...")
                self._migrar_esquema(c)
            
            c.execute("SELECT COUNT(*) FROM ejercicios")
            total = c.fetchone()[0]
            
            if total < 60:
                print(f"📚 Agregando ejercicios ({total} → 60)...")
                self._insertar_ejercicios(c)
            
            c.execute("SELECT COUNT(*) FROM lecciones")
            total_lecciones = c.fetchone()[0]
            
            if total_lecciones < 13:
                print(f"📖 Agregando lecciones ({total_lecciones} → 13)...")
                self._insertar_lecciones(c)
            
            self.conn.commit()
            
            c.execute("SELECT COUNT(*) FROM ejercicios")
            total_final = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM lecciones")
            total_lecciones_final = c.fetchone()[0]
            
            print(f"✓ BD lista: {total_final} ejercicios, {total_lecciones_final} lecciones")
            
            return True, f"{total_final} ejercicios, {total_lecciones_final} lecciones"
            
        except Exception as e:
            print(f"❌ Error inicializando BD: {e}")
            return False, str(e)
        finally:
            self.desconectar()
    
    def _migrar_esquema(self, cursor):
        """Migrar esquema de base de datos"""
        existing_data = []
        try:
            cursor.execute("SELECT * FROM ejercicios")
            existing_data = cursor.fetchall()
        except:
            pass
        
        cursor.execute("DROP TABLE IF EXISTS ejercicios")
        cursor.execute('''CREATE TABLE ejercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            respuesta_correcta TEXT NOT NULL,
            retroalimentacion TEXT,
            dificultad TEXT NOT NULL,
            categoria TEXT NOT NULL,
            materia TEXT NOT NULL DEFAULT 'matematicas',
            pista1 TEXT,
            pista2 TEXT,
            pista3 TEXT,
            puntos INTEGER DEFAULT 10,
            tiempo_estimado INTEGER DEFAULT 60,
            opciones TEXT DEFAULT ''
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS lecciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            materia TEXT NOT NULL,
            dificultad TEXT NOT NULL,
            categoria TEXT NOT NULL,
            contenido TEXT NOT NULL,
            ejemplos TEXT,
            consejos TEXT,
            duracion_minutos INTEGER DEFAULT 10,
            orden INTEGER DEFAULT 0
        )''')
    
    def _insertar_ejercicios(self, cursor):
        """Insertar ejercicios iniciales"""
        from .exercise_data import get_ejercicios_iniciales
        ejercicios = get_ejercicios_iniciales()
        
        cursor.executemany(
            """INSERT INTO ejercicios (pregunta, respuesta_correcta, retroalimentacion, 
               dificultad, categoria, materia, pista1, pista2, pista3, puntos, 
               tiempo_estimado, opciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ejercicios
        )
    
    def _insertar_lecciones(self, cursor):
        """Insertar lecciones iniciales"""
        from .lesson_data import get_lecciones_iniciales
        lecciones = get_lecciones_iniciales()
        
        cursor.execute("DELETE FROM lecciones")
        cursor.executemany(
            """INSERT INTO lecciones (titulo, materia, dificultad, categoria, contenido,
               ejemplos, consejos, duracion_minutos, orden) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            lecciones
        )
    
    def obtener_ejercicios(self, materia=None, dificultad=None, limit=None):
        """Obtener ejercicios filtrados"""
        if not self.conectar():
            return []
        
        try:
            c = self.conn.cursor()
            query = "SELECT * FROM ejercicios WHERE 1=1"
            params = []
            
            if materia:
                query += " AND materia = ?"
                params.append(materia)
            
            if dificultad:
                query += " AND dificultad = ?"
                params.append(dificultad)
            
            query += " ORDER BY RANDOM()"
            
            if limit:
                query += f" LIMIT {limit}"
            
            c.execute(query, params)
            rows = c.fetchall()
            
            return [Exercise(row) for row in rows]
            
        except Exception as e:
            print(f"❌ Error obteniendo ejercicios: {e}")
            return []
        finally:
            self.desconectar()
    
    def obtener_lecciones(self, materia=None, dificultad=None):
        """Obtener lecciones filtradas"""
        if not self.conectar():
            return []
        
        try:
            c = self.conn.cursor()
            query = "SELECT * FROM lecciones WHERE 1=1"
            params = []
            
            if materia:
                query += " AND materia = ?"
                params.append(materia)
            
            if dificultad:
                query += " AND dificultad = ?"
                params.append(dificultad)
            
            query += " ORDER BY orden, id"
            
            c.execute(query, params)
            rows = c.fetchall()
            
            return [Lesson(row) for row in rows]
            
        except Exception as e:
            print(f"❌ Error obteniendo lecciones: {e}")
            return []
        finally:
            self.desconectar()
    
    def contar_ejercicios(self, materia=None, dificultad=None):
        """Contar ejercicios disponibles"""
        if not self.conectar():
            return 0
        
        try:
            c = self.conn.cursor()
            query = "SELECT COUNT(*) FROM ejercicios WHERE 1=1"
            params = []
            
            if materia:
                query += " AND materia = ?"
                params.append(materia)
            
            if dificultad:
                query += " AND dificultad = ?"
                params.append(dificultad)
            
            c.execute(query, params)
            return c.fetchone()[0]
            
        except:
            return 0
        finally:
            self.desconectar()
    
    def contar_lecciones(self, materia=None, dificultad=None):
        """Contar lecciones disponibles"""
        if not self.conectar():
            return 0
        
        try:
            c = self.conn.cursor()
            query = "SELECT COUNT(*) FROM lecciones WHERE 1=1"
            params = []
            
            if materia:
                query += " AND materia = ?"
                params.append(materia)
            
            if dificultad:
                query += " AND dificultad = ?"
                params.append(dificultad)
            
            c.execute(query, params)
            return c.fetchone()[0]
            
        except:
            return 0
        finally:
            self.desconectar()
    
    def validar(self):
        """Validar integridad de la base de datos"""
        if not os.path.exists(self.db_path):
            return False, "Base de datos no encontrada"
        
        if not self.conectar():
            return False, "Error de conexión"
        
        try:
            c = self.conn.cursor()
            c.execute("SELECT COUNT(*) FROM ejercicios")
            total = c.fetchone()[0]
            
            if total == 0:
                return False, "Sin ejercicios"
            
            return True, f"OK ({total} ejercicios)"
            
        except Exception as e:
            return False, f"Error: {e}"
        finally:
            self.desconectar()
