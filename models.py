from flask_login import UserMixin
import sqlite3

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email

    @staticmethod
    def obtener_por_email(email):
        conexion = sqlite3.connect("database/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, email FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        conexion.close()
        if row:
            return Usuario(*row)
        return None