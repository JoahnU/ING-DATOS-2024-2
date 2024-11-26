from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, DECIMAL, Date, Time, TIMESTAMP, Boolean, func, DateTime
)
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabla Jugador
class Jugador(Base):
    __tablename__ = "jugador"
    
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_type = Column(Boolean, default = 0)
    email_address = Column(String(150), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    balance = Column(DECIMAL(10, 2), default=0.00)
    referral_id = Column(Integer, ForeignKey("jugador.player_id", ondelete="SET NULL"))
    earnings = Column(DECIMAL(10, 2), default=0.00)
    
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
    game_name = Column(String, default = 'Roulette')
    min_apuesta = Column(DECIMAL(10, 2), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    hora_juego = Column(Time, nullable=False)
    capacidad = Column(Integer, nullable=False)
    creador_id = Column(Integer, ForeignKey("jugador.player_id", ondelete="CASCADE"), nullable=False)
    resultado = Column(Integer, default=-1)
    color = Column(Integer, nullable=True)
    
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
    color = Column(Integer, nullable=False)

    # Relaciones
    jugador = relationship("Jugador", back_populates="apuestas")
    juego = relationship("Juegos", back_populates="apuestas")


# Tabla intermedia Compra (N:M Jugador <-> Divisas)
class Compra(Base):
    __tablename__ = "compra"
    
    player_id = Column(Integer, ForeignKey("jugador.player_id", ondelete="CASCADE"), primary_key=True)
    div_id = Column(Integer, ForeignKey("divisas.div_id", ondelete="CASCADE"), primary_key=True)
    cantidad = Column(DECIMAL(10, 2), nullable=False)
    fecha = Column(TIMESTAMP, primary_key=True, server_default=func.now())
    
    # Relaciones
    jugador = relationship("Jugador", back_populates="compras")
    divisa = relationship("Divisas", back_populates="compras")


#Creando las tablas del cubo OLAP

class Hechos_Transacciones(Base):
    __tablename__ = "hechos_transacciones"
    transaccion_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer,ForeignKey("Dim_Jugador.dim_jugador_id", ondelete="CASCADE"), nullable=False, autoincrement=True)
    game_id = Column(Integer, ForeignKey("Dim_Juego.dim_juego_id", ondelete="CASCADE"))
    div_id = Column(Integer,ForeignKey("Dim_Divisas.dim_divisas_id", ondelete="CASCADE"))
    cantidad = Column(DECIMAL(10, 2))
    tipo_transaccion = Column(VARCHAR(50), nullable=False)
    tiempo_id = Column(Integer,ForeignKey("Dim_Tiempo.dim_tiempo_id", ondelete="CASCADE"), nullable=False)

    # Relaciones con las dimensiones
    jugador = relationship("Dim_Jugador", backref="hechos_transacciones")
    juego = relationship("Dim_Juego", backref="hechos_transacciones")
    divisa = relationship("Dim_Divisas", backref="hechos_transacciones")
    tiempo = relationship("Dim_Tiempo", backref="hechos_transacciones")

class Dim_Jugador(Base):
    __tablename__ = "Dim_Jugador"
    dim_jugador_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, nullable=False)
    user_name = Column(VARCHAR(100), nullable=False)
    email_address = Column(VARCHAR(150), nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False)
    referral_id = Column(Integer, ForeignKey("Dim_Jugador.dim_jugador_id", ondelete="CASCADE"))
    fecha_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_fin = Column(DateTime(timezone=True))
    estado_actual = Column(Boolean, nullable=False)

    # Relación recursiva para el jugador que refiere
    referido_por = relationship("Dim_Jugador", remote_side=[dim_jugador_id])

class Dim_Juego(Base):
    __tablename__ = "Dim_Juego"

    dim_juego_id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, nullable=False)
    min_apuesta = Column(DECIMAL(10, 2), nullable=False)
    capacidad = Column(Integer, nullable=False)
    total_bet = Column(DECIMAL(10, 2))
    fecha_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_fin = Column(DateTime(timezone=True))
    estado_actual = Column(Boolean, nullable=False)

class Dim_Divisas(Base):
    __tablename__ = "Dim_Divisas"

    dim_divisas_id = Column(Integer, primary_key=True, autoincrement=True)
    div_id = Column(Integer, nullable=False)
    nombre_divisa = Column(VARCHAR(100), nullable=False)
    simbolo_divisa = Column(VARCHAR(10), nullable=False)
    valor_en_monedas = Column(DECIMAL(10, 4), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime)
    estado_actual = Column(Boolean, nullable=False)

class Dim_Tiempo(Base):
    __tablename__ = "Dim_Tiempo"

    dim_tiempo_id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    año = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    dia = Column(Integer, nullable=False)
    dia_semana = Column(VARCHAR(20), nullable=False)
    semana = Column(Integer, nullable=False)
    trimestre = Column(Integer, nullable=False)

# Crear el motor y las tablas (si es necesario)
engine = create_engine("postgresql+psycopg2://postgres:Arg1812@localhost/gambling")
Base.metadata.create_all(engine)
