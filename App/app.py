from flask import Flask, render_template, jsonify, request

# Para autenticación
import jwt 
import datetime

# LLave privada
secret_key = "Gambling4ever"

payload = {
    "user": "Juan Betancourt",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 2),
    "iat": datetime.datetime.utcnow()
}

# Coding token = jwt.encode(payload, secret_key, algorithm="HS256")
# Decoding token = jwt.decode(message. secret_key, algorithms=["HS256"])

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


