from flask import Flask, render_template, jsonify, request, session

# Para autenticación
import jwt 
import datetime

# LLave privada
secret_key = "ilovedbandbandgambling"

payload = {
    "user": "Juan Betancourt",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 2),
    "iat": datetime.datetime.utcnow()
}

# Coding token = jwt.encode(payload, secret_key, algorithm="HS256")
# Decoding token = jwt.decode(message. secret_key, algorithms=["HS256"])

app = Flask(__name__)

app.secret_key = 'Gambling4ever'

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/hola/<nombre>")
def obtenerName(nombre):
    session['nombre'] = nombre
    return f"<h1> Hola {nombre}</h1>"


@app.route("/validando")
def saludoPersonalizado():
        if 'nombre' in session:
            return f"<h1> Hola {session['nombre']}</h1>"
        return "No te conozco"

@app.route("/close")
def cerrarSesion():
    session.clear()
    return "session cleared"

