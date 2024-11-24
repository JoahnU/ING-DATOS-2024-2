from models import engine

from sqlalchemy import text

procedures = [
    # Procedimiento para compra de divisas
    """
        CREATE OR REPLACE PROCEDURE buyCurrency(customer INTEGER, divisa INTEGER, quantity NUMERIC(10,2)) AS $$
        DECLARE
            aumento NUMERIC;   
        BEGIN
            -- Calculando aumento
            aumento := quantity * (SELECT valor_en_monedas FROM divisas WHERE div_id = divisa);
            
            -- Insertando en tabla de compra
            INSERT INTO compra 
            VALUES (customer, divisa, quantity, NOW());

            -- Añadiendo lo equivalente al valor comprado al balance
            UPDATE jugador 
            SET balance = balance + aumento
            WHERE player_id = customer;

        END; 
        $$ LANGUAGE plpgsql;
    """
]


with engine.connect() as connection:
    for procedure in procedures:
        connection.execute(text(procedure))