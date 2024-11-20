from models import *


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


#create

def registrarUsuario(name, email, password):
    nuevoJugador = Jugador(
        user_name = name, 
        email_adress = email

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
    players = session.query(Jugador).all()
    for player in players:
        print(player.user_name, player.email_address)


def rjugador_email(email_address):
    player = session.query(Jugador).filter(Jugador.email_address=="player@gmail.com").first()
    print(player.user_name, player.player_id)



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




