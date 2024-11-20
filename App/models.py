from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, DECIMAL, Date, Time, TIMESTAMP
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabla Jugador
class Jugador(Base):
    __tablename__ = "jugador"
    
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    email_address = Column(String(150), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    balance = Column(DECIMAL(10, 2), default=0.00)
    referral_id = Column(Integer, ForeignKey("jugador.player_id", ondelete="SET NULL"))
    
    # Relaciones
    referidos = relationship("Jugador", remote_side=[player_id])  # Recursiva
    juegos_creados = relationship("Juegos", back_populates="creador")
    apuestas = relationship("Apuesta", back_populates="jugador")
    compras = relationship("Compra", back_populates="jugador")


# Tabla Juegos
class Juegos(Base):
    __tablename__ = "juegos"
    
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    total_bet = Column(DECIMAL(10, 2), default=0.00)
    min_apuesta = Column(DECIMAL(10, 2), nullable=False)
    fecha_creacion = Column(Date, nullable=False)
    hora_juego = Column(Time, nullable=False)
    capacidad = Column(Integer, nullable=False)
    creador_id = Column(Integer, ForeignKey("jugador.player_id", ondelete="CASCADE"), nullable=False)
    
    # Relaciones
    creador = relationship("Jugador", back_populates="juegos_creados")
    apuestas = relationship("Apuesta", back_populates="juego")


# Tabla Divisas
class Divisas(Base):
    __tablename__ = "divisas"
    
    div_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_divisa = Column(String(100), nullable=False)
    simbolo_divisa = Column(String(10), nullable=False, unique=True)
    valor_en_monedas = Column(DECIMAL(10, 4), nullable=False)
    
    # Relaciones
    compras = relationship("Compra", back_populates="divisa")


# Tabla intermedia Apuesta (N:M Jugador <-> Juegos)
class Apuesta(Base):
    __tablename__ = "apuesta"
    
    player_id = Column(Integer, ForeignKey("jugador.player_id", ondelete="CASCADE"), primary_key=True)
    game_id = Column(Integer, ForeignKey("juegos.game_id", ondelete="CASCADE"), primary_key=True)
    valor = Column(DECIMAL(10, 2), default=0.00)
    numero = Column(Integer)

    # Relaciones
    jugador = relationship("Jugador", back_populates="apuestas")
    juego = relationship("Juegos", back_populates="apuestas")


# Tabla intermedia Compra (N:M Jugador <-> Divisas)
class Compra(Base):
    __tablename__ = "compra"
    
    player_id = Column(Integer, ForeignKey("jugador.player_id", ondelete="CASCADE"), primary_key=True)
    div_id = Column(Integer, ForeignKey("divisas.div_id", ondelete="CASCADE"), primary_key=True)
    cantidad = Column(DECIMAL(10, 2), nullable=False)
    fecha = Column(TIMESTAMP, primary_key=True)
    
    # Relaciones
    jugador = relationship("Jugador", back_populates="compras")
    divisa = relationship("Divisas", back_populates="compras")


# Crear el motor y las tablas (si es necesario)
engine = create_engine("postgresql+psycopg2://postgres:password@localhost/gambling")
Base.metadata.create_all(engine)
