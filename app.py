from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    return "¡Aplicación Flask funcionando! Visita /usuario para tu saludo."

# Ruta de usuario con parámetro opcional
@app.route('/usuario/', defaults={'nombre': 'Invitado'})
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template('usuario.html', nombre=nombre)

# Ruta con formulario para que el usuario ingrese su nombre
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form.get('nombre', 'Invitado')
        return render_template('usuario.html', nombre=nombre)
    return '''
        <form method="POST">
            Ingresa tu nombre: <input type="text" name="nombre">
            <input type="submit" value="Enviar">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
