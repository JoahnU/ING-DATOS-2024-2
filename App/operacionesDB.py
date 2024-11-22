from models import *
import hashlib

from sqlalchemy import Date, cast
from datetime import date


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


def crearjuegos(nombre, hora, min_apuesta,capacidad, creator_id ):
    nuevojuego = Juegos(
        min_apuesta= min_apuesta,
        capacidad = capacidad,
        creador_id = creator_id,
        hora_juego = hora, 
        game_name = nombre
    )
    session.add(nuevojuego)
    session.commit()
    return nuevojuego

def nuevapuesta(p_id, g_id, valor, numero):
    nuevapuesta = Apuesta(
        player_id = p_id,
        game_id = g_id,
        valor= valor,
        numero = numero
    )
    session.add(nuevapuesta)
    session.commit()
    return nuevapuesta

def compras(player_id, div_id, cantidad):

    nuevacompra = Compra(
        player_id= player_id,
        div_id= 1,
        cantidad= cantidad,

    )
    session.add(nuevacompra)
    session.commit()
    return nuevacompra

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


def get_games_avaiable():
    # Query para buscar los juegos de la fecha actual
    player_games = (
        session.query(Juegos)
        .filter(cast(Juegos.fecha_creacion,Date) == date.today()).all()
    )
    return player_games


#update 
def update_player_balance(session, player_name, amount):
    
    # Buscar el jugador por nombre
    player = session.query(Jugador).filter(Jugador.user_name == player_name).first()
    
    if player:
        # Actualizar el balance del jugador
        player.balance += amount
        session.commit()
        return f"El balance de {player_name} se actualizó a {player.balance:.2f}."
    else:
        return f"No se encontró un jugador con el nombre '{player_name}'."


#delete


def delete_player(session, player_name):
    
    # Buscar el jugador por nombre
    player = session.query(Jugador).filter(Jugador.user_name == player_name).first()
    
    if player:
        # Eliminar el jugador si existe
        session.delete(player)
        session.commit()
        return f"El jugador '{player_name}' fue eliminado exitosamente."
    else:
        return f"No se encontró un jugador con el nombre '{player_name}'."


#acceder referridos
def get_player_referrals(session, player_name):
    
    # Buscar al jugador por su nombre
    player = session.query(Jugador).filter(Jugador.user_name == player_name).first()
    
    if player:
        # Obtener los referidos del jugador
        referrals = [{"user_name": referral.user_name, "email_address": referral.email_address}
                     for referral in player.referidos]
        
        # Retornar la lista de referidos
        return referrals
    else:
        return f"No se encontró un jugador con el nombre '{player_name}'."

#juegos y sus apuestas

def get_game_bets(session, game_id):
    
    # Buscar el juego por su ID
    game = session.query(Juegos).filter(Juegos.game_id == game_id).first()
    
    if game:
        # Obtener las apuestas asociadas al juego
        bets = [{"user_name": bet.jugador.user_name, "game_id": bet.game_id}
                for bet in game.apuestas]
        
        return bets
    else:
        return f"No se encontró un juego con el ID {game_id}."



def get_available_games(session):
    """
    Retorna una lista de todos los juegos disponibles para unirse.
    Un juego está disponible si la cantidad de jugadores actuales es menor que su capacidad.
    """
    from sqlalchemy.sql import func  # Para usar funciones como COUNT

    # Subconsulta para contar jugadores en cada juego
    subquery = (
        session.query(
            Apuesta.game_id,
            func.count(Apuesta.player_id).label("current_players")
        )
        .group_by(Apuesta.game_id)  # Agrupar por ID del juego
        .subquery()
    )

    # Consulta principal para juegos disponibles
    available_games = (
        session.query(Juegos)
        .outerjoin(subquery, Juegos.game_id == subquery.c.game_id)  # Unión con subconsulta
        .filter(
            func.coalesce(subquery.c.current_players, 0) < Juegos.capacidad  # Comparar capacidad
        )
        .all()
    )
    
    # Formatear la respuesta como lista de diccionarios (opcional)
    result = [
        {
            "game_id": game.game_id,
            "min_apuesta": game.min_apuesta,
            "capacidad": game.capacidad,
            "current_players": subquery.c.current_players if subquery.c.current_players else 0,
            "creador_id": game.creador_id,
        }
        for game in available_games
    ]
    
    return result
