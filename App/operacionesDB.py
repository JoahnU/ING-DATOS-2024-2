from models import Jugador, engine


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

def registrarUsuario(name, email, password):
    nuevoJugador = Jugador(
        user_name = name, 
        email_adress = email

    )
    session.add(nuevoJugador)
    return session.commit()
