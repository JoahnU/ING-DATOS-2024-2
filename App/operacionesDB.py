from models import *
import hashlib


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


#create

def registrarUsuario(name, email, password):
    nuevoJugador = Jugador(
        user_name = name, 
        email_address = email,
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    )
    session.add(nuevoJugador)
    session.commit()
    return nuevoJugador


def crearjuegos(min_apuesta,capacidad, creator_id ):
    nuevojuego = Juegos(
        total_bet = 0,
        min_apuesta= min_apuesta,
        capacidad = capacidad,
        creador_id = creator_id

    )
    session.add(nuevojuego)
    session.commit()

def nuevapuesta(p_id, g_id, valor, numero):
    nuevapuesta = Apuesta(
        player_id = p_id,
        game_id = g_id,
        valor= valor,
        numero = numero
    )
    session.add(nuevapuesta)
    session.commit()

def compras(player_id, div_id, cantidad):

    nuevacompra = Compra(
        player_id= player_id,
        div_id= 1,
        cantidad= cantidad,

    )
    session.add(nuevacompra)
    session.commit()


#read

def rjugador_id(player_id):
    player = session.query(Jugador).filter(Jugador.player_id==player_id).first()
    return player


def rjugador_email(email_address):
    player = session.query(Jugador).filter(Jugador.email_address==email_address).first()
    return player



def get_games_by_player(session, player_name):
    
    # Query para buscar los juegos creados por el jugador
    player_games = (
        session.query(Juegos)
        .join(Jugador)  # Realiza el join entre Juegos y Jugador
        .filter(Jugador.user_name == player_name)  # Filtra por el nombre del jugador
        .all()  # Devuelve todos los resultados como una lista
    )
    
    return player_games



#update 
