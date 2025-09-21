from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario
import sqlite3

app = Flask(__name__)
app.secret_key = "mi_clave_secreta"

# -------------------------------  
# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_email(user_id)

# -------------------------------  
# Ruta principal: agregar usuario
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]

        conn = sqlite3.connect("database/usuarios.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", 
                       (nombre, email, generate_password_hash("1234")))  # contraseña por defecto
        conn.commit()
        conn.close()
    
        flash("Usuario agregado correctamente!")
        return redirect("/usuarios")

    return render_template("usuario.html")

# -------------------------------  
# Mostrar todos los usuarios
@app.route("/usuarios")
def mostrar_usuarios():
    conn = sqlite3.connect("database/usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template("usuarios.html", usuarios=usuarios)

# -------------------------------  
# Registro de usuario
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        Usuario.crear(nombre, email, password)
        flash("Usuario registrado con éxito")
        return redirect(url_for("login"))
    return render_template("registro.html")

# -------------------------------  
# Login de usuario
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        usuario = Usuario.obtener_por_email(email)
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash("Sesión iniciada correctamente")
            return redirect(url_for("protegido"))
        else:
            flash("Credenciales incorrectas")
    return render_template("login.html")

# -------------------------------  
# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada")
    return redirect(url_for("login"))

# -------------------------------  
# Ruta protegida
@app.route("/protegido")
@login_required
def protegido():
    return render_template("protegido.html", nombre=current_user.nombre)

# -------------------------------  
if __name__ == "__main__":
    app.run(debug=True)
