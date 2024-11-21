# importando modulos de flask
from flask import (
    Flask, render_template, jsonify, request, session, redirect, url_for
)
import operacionesDB

import hashlib

from sqlalchemy.exc import SQLAlchemyError

# Para autenticación
import jwt 
from datetime import datetime, date, timedelta

# LLave privada
secret_key = "ilovedbandgambling"

# Coding token = jwt.encode(payload, secret_key, algorithm="HS256")
# Decoding token = jwt.decode(message. secret_key, algorithms=["HS256"])

"""
payload = {
    "id": ...,
    "nombre": ...,
    "rol": ...,
    "crDate": ...,
    "expDate": ...
}
"""

app = Flask(__name__)

app.secret_key = 'Gambling4ever'

# Ruta inicial
@app.route("/")
def index():
    if 'jwt' in session:
        return render_template(
            "index.html", user = jwt.decode(
                session['jwt'], 
                secret_key, 
                algorithms=["HS256"]
                )
            )
    return redirect(url_for('login'))

# Login 
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods = ['POST'])
def login_in():
    try:
        user = operacionesDB.rjugador_email(request.form.get('email'))
        password = request.form.get('password')
        hashedpassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user.password == hashedpassword:
            payload = {
            "id": user.player_id,
            "nombre": user.user_name,
            "rol": 'player',
            "crDate": str(datetime.now()),
            "expDate": str(datetime.now() + timedelta(days=2))
            }

            session['jwt'] = jwt.encode(payload, secret_key, algorithm="HS256")

            return redirect(url_for('index'))
        else:
            return render_template("register.html", error = 'Usuario o contraseña no coinciden')
        
    except SQLAlchemyError as e: 
        return render_template("register.html", error = e)


# Registro
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods = ['POST'])
def register_in():
    # Verificando que las contraseñas sean correctas
    if request.form.get('password') != request.form.get('confirmPassword'):
        return render_template("register.html", error = 'Las contraseñas no coinciden')

    try:
        jugador = operacionesDB.registrarUsuario(
            request.form.get('username'), 
            request.form.get('email'),
            request.form.get('password')
        )
        
        payload = {
            "id": jugador.player_id,
            "nombre": jugador.user_name,
            "rol": 'player',
            "crDate": str(datetime.now()),
            "expDate": str(datetime.now() + timedelta(days=2))
        }

        session['jwt'] = jwt.encode(payload, secret_key, algorithm="HS256")

        return redirect(url_for('index'))

    except SQLAlchemyError as e: 
        return render_template("register.html", error = e)


@app.route("/logout")
def cerrarSesion():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
     app.run()