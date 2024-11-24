from database.operacionesDB import engine

from sqlalchemy import text

procedures = [
    
]


with engine.connect() as connection:
    for procedure in procedures:
        connection.execute(text(procedure))