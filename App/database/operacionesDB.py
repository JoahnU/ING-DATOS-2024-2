from database.models import *
import hashlib

from sqlalchemy import Date, cast, text, func
from datetime import date


from sqlalchemy.orm import sessionmaker, aliased
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


def registrarUsuarioReferido(name, email, password, id):
    nuevoJugador = Jugador(
        user_name = name, 
        email_address = email,
        password = hashlib.sha256(password.encode('utf-8')).hexdigest(),
        referral_id = id,
        balance = 50
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

def nuevapuesta(player, game, quantity, color):
    with engine.begin() as connection:
        connection.execute(
            text("CALL apuesta(:player, :game, :quantity, :color);"),
            {
                "player": player,
                "game": int(game),
                "quantity": quantity,
                "color": color.capitalize()
            },
        )
        return True
    
def cancel_bet(player, game):
    with engine.begin() as connection:
        connection.execute(
            text("CALL cancelar_apuesta(:player, :game);"),
            {
                "player": player,
                "game": int(game)
            },
        )
        return True
    
def apuesta_jugador_juego(player, game):
    return session.query(Apuesta).filter(Apuesta.player_id == player).filter(Apuesta.game_id == game).first()


def compras(player_id, div_id, cantidad): 
    # Creando compra mediante procedimiento buyCurrency   
    with engine.begin() as connection:
        connection.execute(
            text("CALL buyCurrency(:player, :divisa, :quantity);"),
            {
                "player": player_id,
                "divisa": div_id,
                "quantity": cantidad,
            },
        )
        return True

    
def resultado(id): 
    # Creando compra mediante procedimiento buyCurrency   
    with engine.begin() as connection:
        return connection.execute(
            text("SELECT getResult(:id);"),
            {
                "id": id,
            }
        ).fetchone()[0]
    
def historial_balance(id): 
    # Creando compra mediante procedimiento buyCurrency   
    with engine.begin() as connection:
        return connection.execute(
            text("SELECT * FROM historial_balance(:id);"),
            {
                "id": id,
            }
        ).all()

def data_app(): 
    # Creando compra mediante procedimiento buyCurrency   
    with engine.begin() as connection:
        return connection.execute(
            text("SELECT * FROM hechos;")
        ).all()

#read
def rjugador_id(player_id):
    player = session.query(Jugador).filter(Jugador.player_id==player_id).first()
    return player


def rjugador_email(email_address):
    player = session.query(Jugador).filter(Jugador.email_address==email_address).first()
    return player



def get_game_by_id(id):
    return session.query(Juegos).filter(Juegos.game_id==id).first()



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
        session.query(Juegos, func.count(Apuesta.game_id).label("numero_apuestas"))
        .outerjoin(Apuesta, Juegos.game_id == Apuesta.game_id)
        .filter(cast(Juegos.fecha_creacion, Date) == date.today())
        .group_by(Juegos.game_id)
        .all()
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
        return True
    else: False


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
def get_player_referrals(id):
    # Alias para la consulta
    referred = aliased(Jugador);
    
    # Buscar al jugador por su nombre
    query = session.query(Jugador, referred).join(referred, Jugador.player_id == referred.referral_id).filter(Jugador.player_id == id)

    # Retornando unicamente la información de los referidos
    return [ player for _, player in query.all() ]

#juegos y sus apuestas

def get_game_bets(game_id):
    
    # Buscar el juego por su ID
    game = session.query(Juegos).filter(Juegos.game_id == game_id).first()
    
    if game:
        # Obtener las apuestas asociadas al juego
        bets = [{"user_name": bet.jugador.user_name, "game_id": bet.game_id}
                for bet in game.apuestas]
        
        return bets
    else:
        return None



def get_available_games():
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
            "current_players": subquery.c.current_players,
            "creador_id": game.creador_id,
            "hora_juego": game.hora_juego
        }
        for game in available_games
    ]
    
    return result


def get_divisas(): 
    return session.query(Divisas).all()