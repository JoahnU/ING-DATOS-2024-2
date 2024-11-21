# importando modulos de flask
from flask import (
    Flask, render_template, jsonify, request, session, redirect, url_for
)

# Hasheo 
import hashlib

# Operaciones con bases de datos
import operacionesDB as operacionesDB
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

# Creando aplicación 
app = Flask(__name__)

# Añadiendo palabra clave para variables de sesión
app.secret_key = 'Gambling4ever'

# Middleware para cerrar sesiones expiradas
@app.before_request
def middleware():
    # Verificando que haya un web token
    if 'jwt' in session:
        # Decodeando el token
        user = jwt.decode (
            session['jwt'], 
            secret_key, 
            algorithms=["HS256"]
        )
        # Sí la fecha ya pasó limpiamos la sesión
        if datetime.strptime(user['expDate'].split('.')[0], '%Y-%m-%d %H:%M:%S') < datetime.now(): 
            session.clear()



# Ruta inicial
@app.route("/")
def index():
    # Dependiendo si tiene el web token
    if 'jwt' in session:
        user = jwt.decode (
                session['jwt'], 
                secret_key, 
                algorithms=["HS256"]
        )
        # Renderizando template con payload
        if user['rol'] == 1:
            return render_template("indexAdmin.html", user = user)
        return render_template("index.html", user = user)
    # Si no hay web token redireccionamos al login
    return redirect(url_for('login'))

# Login 
@app.route("/login")
def login():
    # Template de inicio de sesión
    return render_template("login.html")

@app.route("/login", methods = ['POST'])
def login_in():
    try:
        user = operacionesDB.rjugador_email(request.form.get('email'))
        if user is None:
            return render_template("login.html", error = 'Usuario o contraseña no coinciden')
        password = request.form.get('password')
        hashedpassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user.password == hashedpassword:
            payload = {
            "id": user.player_id,
            "nombre": user.user_name,
            "rol": user.user_type,
            "crDate": str(datetime.now()),
            "expDate": str(datetime.now() + timedelta(days=2))
            }

            session['jwt'] = jwt.encode(payload, secret_key, algorithm="HS256")

            return redirect(url_for('index'))
        else:
            return render_template("login.html", error = 'Usuario o contraseña no coinciden')
        
    except SQLAlchemyError as e: 
        operacionesDB.session.rollback()
        return render_template("login.html", error = e)


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
        operacionesDB.session.rollback()
        return render_template("register.html", error = e)
    

    
@app.route("/crear", methods = ['GET'])
def crearJuegos():
    if 'jwt' not in session:
        return redirect(url_for('index'))
    
    return render_template("creategames.html")

@app.route("/crear",methods = ['POST'])
def crearDB():
    if 'jwt' not in session:
        return redirect(url_for('index'))
    
    user = jwt.decode (
        session['jwt'], 
        secret_key, 
        algorithms=["HS256"]
    )
    
    try:
        operacionesDB.crearjuegos(
            request.form.get('game_name'),
            request.form.get('game_time'),
            request.form.get('min_bet'),
            request.form.get('capacity'),
            user['id']
            )
        return redirect(url_for('index'))
    except SQLAlchemyError as e: 
        return render_template(
            "creategames.html", 
            error = e, 
            form = request.form
        )

@app.route("/logout")
def cerrarSesion():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()