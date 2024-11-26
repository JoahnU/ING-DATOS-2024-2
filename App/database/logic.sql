CREATE OR REPLACE PROCEDURE buyCurrency(customer INTEGER, divisa INTEGER, quantity NUMERIC(10,2)) AS $$
DECLARE
    aumento NUMERIC;  
	date_id INT;
	id_player INT; 
	divisa_id INT;
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

	-- Obteniendo id de la dimension fecha, jugador y divisas
	IF (SELECT COUNT(*) FROM "Dim_Tiempo" WHERE fecha = CURRENT_DATE) = 0 THEN 
		PERFORM dim_tiempo();
	END IF;

	date_id := (SELECT dim_tiempo_id FROM "Dim_Tiempo" WHERE fecha = CURRENT_DATE LIMIT 1);
	id_player := (SELECT dim_jugador_id FROM "Dim_Jugador" WHERE player_id = customer AND fecha_fin IS NULL LIMIT 1);
	divisa_id := (SELECT dim_divisas_id FROM "Dim_Divisas" WHERE div_id = divisa  AND fecha_fin IS NULL LIMIT 1);
	
	-- Actualizando la tabla de hechos 
	INSERT INTO hechos_transacciones (player_id, div_id, cantidad, tipo_transaccion, tiempo_id)
	VALUES (id_player, divisa_id, quantity, 'Compra', date_id);

	RETURN;
END; 
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION dim_tiempo()
RETURNS VOID AS $$
DECLARE
    current_date DATE;
    year INT;
    month INT;
    day INT;
    day_name VARCHAR(20);
    week INT;
    quarter INT;
BEGIN
    current_date := CURRENT_DATE;

	-- Calculate derived values
	year := EXTRACT(YEAR FROM current_date);
	month := EXTRACT(MONTH FROM current_date);
	day := EXTRACT(DAY FROM current_date);
	day_name := TO_CHAR(current_date, 'FMDay');  -- Full day name
	week := EXTRACT(WEEK FROM current_date);
	quarter := EXTRACT(QUARTER FROM current_date);

	-- Insert into Dim_Tiempo
	INSERT INTO "Dim_Tiempo" (fecha, año, mes, dia, dia_semana, semana, trimestre)
	VALUES (current_date, year, month, day, day_name, week, quarter);

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION crear_dim_divisas()
RETURNS TRIGGER AS $$
BEGIN
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

CREATE TRIGGER trg_crear_dim_divisas
AFTER INSERT
ON Divisas
FOR EACH ROW
EXECUTE FUNCTION crear_dim_divisas();


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


CREATE OR REPLACE FUNCTION crear_dim_divisas()
RETURNS TRIGGER AS $$
BEGIN
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

CREATE TRIGGER trg_crear_dim_divisas
AFTER INSERT
ON Divisas
FOR EACH ROW
EXECUTE FUNCTION crear_dim_divisas();

-- Función para obtener resultado de un juego 
CREATE OR REPLACE FUNCTION getResult(id INT) RETURNS INT AS $$
DECLARE 
	resultado_valor INT;
	horaJuego TIME;
BEGIN 
	resultado_valor := (SELECT resultado FROM juegos WHERE game_id = id LIMIT 1);
	horaJuego := (SELECT hora_juego FROM juegos WHERE game_id = id LIMIT 1);

	IF resultado_valor = -1 AND horaJuego <= NOW()::TIME THEN
		UPDATE juegos SET resultado = (RANDOM()*37)::int WHERE game_id = id;
		resultado_valor := (SELECT resultado FROM juegos WHERE game_id = id LIMIT 1);
	END IF;

	RETURN resultado_valor;

END;
$$ LANGUAGE plpgsql;

-- Funcion para saber el color ganador

CREATE OR REPLACE FUNCTION get_number_color(number INT)
RETURNS TEXT AS $$
BEGIN
    IF number = 0 THEN
        RETURN 'Green';
    ELSIF number IN (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36) THEN
        RETURN 'Red';
    ELSIF number IN (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35) THEN
        RETURN 'Black';
    ELSE
        RETURN 'Unknown';
    END IF;
END;
$$ LANGUAGE plpgsql;

--para incrementar el balance de los referidos

CREATE OR REPLACE PROCEDURE incrementarBalance(
    user_id INTEGER, 
    cantidad NUMERIC(10, 2)
)
AS $$
DECLARE
    referido_id INTEGER;
    recompensa NUMERIC(10, 2);
BEGIN
    
    UPDATE jugador
    SET balance = balance + cantidad, earnings = earnings + cantidad
    WHERE player_id = user_id;

    
    SELECT referral_id INTO referido_id
    FROM jugador
    WHERE player_id = user_id;

	
	-- Creando en la dimension de tiempo el registro en caso de no existir
	IF (SELECT COUNT(*) FROM "Dim_Tiempo" WHERE fecha = CURRENT_DATE) = 0 THEN 
		PERFORM dim_tiempo();
	END IF;

    -- Aumentando el 5% de ganancias a el usuario que lo refirió
    IF referido_id IS NOT NULL THEN
        recompensa := cantidad * 0.05;

        UPDATE jugador
        SET balance = balance + recompensa
        WHERE player_id = referido_id;

        
        INSERT INTO hechos_transacciones (player_id, cantidad, tipo_transaccion, tiempo_id)
        VALUES (
            (SELECT dim_jugador_id FROM "Dim_Jugador" WHERE player_id = referido_id AND fecha_fin IS NULL LIMIT 1), 
            recompensa, 
            'Aumento por referido',
            (SELECT dim_tiempo_id FROM "Dim_Tiempo" WHERE fecha = CURRENT_DATE LIMIT 1)
        );
    END IF;

   -- Registrando hecho en OLAP
    INSERT INTO hechos_transacciones (player_id, cantidad, tipo_transaccion, tiempo_id)
    VALUES (
        (SELECT dim_jugador_id FROM "Dim_Jugador" WHERE player_id = user_id AND fecha_fin IS NULL LIMIT 1), 
        cantidad, 
        'premio victoria', 
        (SELECT dim_tiempo_id FROM "Dim_Tiempo" WHERE fecha = CURRENT_DATE LIMIT 1)
    );

END;
$$ LANGUAGE plpgsql;