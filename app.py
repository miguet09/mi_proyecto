from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "mi_clave_secreta"  # necesaria para usar flash

# -------------------------------
# Ruta principal: agregar usuario
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]

        # Conectar a la base de datos y agregar usuario
        conn = sqlite3.connect("database/usuarios.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
        conn.commit()
        conn.close()
    
        flash("Usuario agregado correctamente!")  # <-- mensaje de confirmación

        return redirect("/usuarios")  # Redirige automáticamente a la lista de usuarios

    # Mostrar formulario
    return render_template("usuario.html")

# -------------------------------
# Ruta para mostrar todos los usuarios
@app.route("/usuarios")
def mostrar_usuarios():
    conn = sqlite3.connect("database/usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template("usuarios.html", usuarios=usuarios)

# -------------------------------
if __name__ == "__main__":
    app.run(debug=True) 
