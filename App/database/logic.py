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
    """,
    """
        CREATE OR REPLACE FUNCTION crear_dim_jugador()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Insertar un nuevo registro en Dim_Jugador
            INSERT INTO "Dim_Jugador" (player_id, user_name, email_address, balance, fecha_inicio, estado_actual)
            VALUES (
                NEW.player_id, 
                NEW.user_name, 
                NEW.email_address, 
                NEW.balance, 
                NOW(), 
                TRUE
            );

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_crear_dim_jugador
        AFTER INSERT
        ON Jugador
        FOR EACH ROW
        EXECUTE FUNCTION crear_dim_jugador();
    """,
    """
        CREATE OR REPLACE FUNCTION actualizar_dim_jugador()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Cerrar el registro actual en Dim_Jugador
            UPDATE "Dim_Jugador"
            SET fecha_fin = NOW(), estado_actual = FALSE
            WHERE player_id = NEW.player_id AND estado_actual = TRUE;

            -- Insertar un nuevo registro en Dim_Jugador
            INSERT INTO "Dim_Jugador" (player_id, user_name, email_address, balance, fecha_inicio, estado_actual)
            VALUES (
                NEW.player_id, 
                NEW.user_name, 
                NEW.email_address, 
                NEW.balance, 
                NOW(), 
                TRUE
            );

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_actualizar_dim_jugador
        AFTER UPDATE OF user_name, email_address, balance
        ON Jugador
        FOR EACH ROW
        EXECUTE FUNCTION actualizar_dim_jugador();
    """,
    """
        CREATE OR REPLACE FUNCTION actualizar_dim_juegos()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Cerrar el registro actual en Dim_Juegos
            UPDATE "Dim_Juegos"
            SET fecha_fin = NOW(), estado_actual = FALSE
            WHERE game_id = NEW.game_id AND estado_actual = TRUE;

            -- Insertar un nuevo registro en Dim_Juegos
            INSERT INTO "Dim_Juegos" (game_id, min_apuesta, capacidad, fecha_inicio, estado_actual)
            VALUES (
                NEW.game_id, 
                NEW.min_apuesta, 
                NEW.capacidad, 
                NOW(), 
                TRUE
            );

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_actualizar_dim_juegos
        AFTER UPDATE OF min_apuesta, capacidad
        ON Juegos
        FOR EACH ROW
        EXECUTE FUNCTION actualizar_dim_juegos();
    """,
    """
        CREATE OR REPLACE FUNCTION actualizar_dim_divisas()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Cerrar el registro actual en Dim_Divisas
            UPDATE "Dim_Divisas"
            SET fecha_fin = NOW(), estado_actual = FALSE
            WHERE div_id = NEW.div_id AND estado_actual = TRUE;

            -- Insertar un nuevo registro en Dim_Divisas
            INSERT INTO "Dim_Divisas" (div_id, nombre_divisa, simbolo_divisa, valor_en_monedas, fecha_inicio, estado_actual)
            VALUES (
                NEW.div_id, 
                NEW.nombre_divisa, 
                NEW.simbolo_divisa, 
                NEW.valor_en_monedas, 
                NOW(), 
                TRUE
            );

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_actualizar_dim_divisas
        AFTER UPDATE OF valor_en_monedas
        ON Divisas
        FOR EACH ROW
        EXECUTE FUNCTION actualizar_dim_divisas();
    """
]


with engine.connect() as connection:
    for procedure in procedures:
        connection.execute(text(procedure))