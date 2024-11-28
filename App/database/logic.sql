-- Procedimiento que aumenta el balance de un jugador hecha una compra bajo una divisa
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

-- Función encargada de poblar la dimension de tiempo
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

-- Triggerer que pobla la dimensión de divisas al crearse una divisa
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

-- Triggerer que pobla la dimensión de jugadores al crear un jugador
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

-- Triggerer que pobla la dimension de jugador al actualizar un jugador 
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

-- Triggerer que pobla la dimension de juego una vez se actualizan datos sobre el juego
CREATE OR REPLACE FUNCTION actualizar_dim_juegos()
RETURNS TRIGGER AS $$
BEGIN
    -- Cerrar el registro actual en Dim_Juegos
    UPDATE "Dim_Juego"
    SET fecha_fin = NOW(), estado_actual = FALSE
    WHERE game_id = NEW.game_id AND estado_actual = TRUE;

    -- Insertar un nuevo registro en Dim_Juegos
    INSERT INTO "Dim_Juego" (game_id, min_apuesta, capacidad, fecha_inicio, estado_actual)
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


-- Triggerer que pobla la dimension de juego una vez se crea un juego
CREATE OR REPLACE FUNCTION Crear_dim_juegos()
RETURNS TRIGGER AS $$
BEGIN
    -- Insertar un nuevo registro en Dim_Juegos
    INSERT INTO "Dim_Juego" (game_id, min_apuesta, capacidad, fecha_inicio, estado_actual)
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

CREATE TRIGGER trg_crear_dim_juegos
AFTER INSERT
ON Juegos
FOR EACH ROW
EXECUTE FUNCTION Crear_dim_juegos();


-- Trigger que se encarga de poblar dimension de divisas una vez se actualize un dato de estas
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
RETURNS VARCHAR(10) AS $$
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

    -- Aumentando el 10% de ganancias a el usuario que lo refirió
    IF referido_id IS NOT NULL THEN
        recompensa := cantidad * 0.10;

        UPDATE jugador
        SET balance = balance + recompensa,
            earnings = earnings + recompensa
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


-- Procedure para crear una apuesta
CREATE OR REPLACE PROCEDURE apuesta(player INT, game INT, quantity NUMERIC(10,2), color VARCHAR(10)) AS $$
BEGIN 
	-- Validando que haya saldo suficiente y cupos disponibles para realizar apuesta
	IF (SELECT balance FROM jugador WHERE player_id = player) < quantity THEN 
		RAISE EXCEPTION 'Saldo insuficiente para hacer apuesta';
	ELSIF ((SELECT COUNT(*) FROM apuesta WHERE game_id = game) >= (SELECT capacidad FROM juegos WHERE game_id = game)) THEN 
		RAISE EXCEPTION 'Cupos insuficientes para hacer la apuesta';
	ELSIF (SELECT resultado FROM juegos WHERE game_id = game) != -1 THEN
		RAISE EXCEPTION 'El resultado de este juego ya ha sido dado';
	ELSIF (SELECT min_apuesta FROM juegos WHERE game_id = game) > quantity THEN
		RAISE EXCEPTION 'La apuesta es menor a la apuesta mínima';
	ELSIF (SELECT hora_juego FROM juegos WHERE game_id = game) < NOW()::TIME THEN
		RAISE EXCEPTION 'No se puede apostar después de la hora limite';
	END IF; 

	-- Quitando valor apostado al saldo del jugador 
	UPDATE jugador SET balance = balance - quantity WHERE player_id = player; 
	
	-- Creando el registro de la apuesta
	INSERT INTO apuesta VALUES (player, game, quantity, color); 
	
	-- Sumando valor apostado a apuesta total del juego
	UPDATE juegos SET total_bet = total_bet + quantity WHERE game_id = game;
	
	
	-- Registrando transacción en OLAP 
	INSERT INTO hechos_transacciones (player_id, game_id, cantidad, tipo_transaccion, tiempo_id)
    VALUES (
        (SELECT dim_jugador_id FROM "Dim_Jugador" WHERE player_id = player AND fecha_fin IS NULL LIMIT 1), 
		(SELECT dim_juego_id FROM "Dim_Juego" WHERE game_id = game AND fecha_fin IS NULL LIMIT 1),
        quantity, 
        'Apuesta', 
        (SELECT dim_tiempo_id FROM "Dim_Tiempo" WHERE fecha = CURRENT_DATE LIMIT 1)
    ); 

	RETURN; 
END;
$$ LANGUAGE plpgsql;

-- Triggerer que premia a los ganadores una vez hay resultado en un juego 
CREATE OR REPLACE FUNCTION ganadores() RETURNS TRIGGER AS $$
DECLARE 
	color_result VARCHAR(10);
	bonificacion INT;
	apuesta_pl RECORD;
BEGIN 

	-- Añadiendo el color resultante a el registro del juego
	color_result := get_number_color(NEW.resultado);
	UPDATE juegos SET color = color_result WHERE game_id = NEW.game_id; 

	IF color_result NOT IN ('Red', 'Green', 'Black') THEN 
		RAISE EXCEPTION 'Resultado no posible';
	END IF; 

	-- Decidiendo bonificacion para ganadores
	IF color_result = 'Green' THEN
		bonificacion := 36;
	ELSE 
		bonificacion:= 2;
	END IF; 

	-- Creando tabla temporal
	CREATE TEMP TABLE apuestas_ganadoras (id INT, quantity NUMERIC(10,2));
	
	-- Obteniendo id de ganadores y cantidad apostada
	INSERT INTO apuestas_ganadoras SELECT player_id, valor FROM apuesta WHERE game_id = NEW.game_id AND color = color_result;

	-- Aumentando balance de acuerdo a lo ganado
	FOR apuesta_pl IN SELECT * FROM apuestas_ganadoras LOOP 
		CALL incrementarbalance(apuesta_pl.id, apuesta_pl.quantity * bonificacion);
	END LOOP;

	RETURN NEW; 
	
END;
$$ LANGUAGE plpgsql; 


-- Funcion para obtener el historial de balance de un jugador 
CREATE OR REPLACE FUNCTION historial_balance(id INT) RETURNS TABLE(balance NUMERIC(10,2), cantidad NUMERIC(10,2), hecho VARCHAR(10)) AS $$
BEGIN 
	RETURN query
			SELECT dim.balance as Nuevo_balance, hecho.cantidad, hecho.tipo_transaccion FROM "Dim_Jugador" dim 
			JOIN hechos_transacciones hecho
			ON dim.dim_jugador_id = hecho.player_id
			WHERE dim.player_id = id
            ORDER BY hecho.transaccion_id DESC;
END; 
$$ LANGUAGE plpgsql;
TABLE juegos;


-- Procedure para crear una apuesta
CREATE OR REPLACE PROCEDURE cancelar_apuesta(player INT, game INT) AS $$
DECLARE 
	quantity INT;
BEGIN 
	-- Validando que haya saldo suficiente y cupos disponibles para realizar apuesta
	IF (SELECT resultado FROM juegos WHERE game_id = game) != -1 THEN
		RAISE EXCEPTION 'El resultado de este juego ya ha sido dado';
	ELSIF (SELECT hora_juego FROM juegos WHERE game_id = game) < NOW()::TIME THEN
		RAISE EXCEPTION 'No se puede apostar después de la hora limite';
	END IF; 

	-- Obteniendo cantidad apostada
	quantity := (SELECT valor FROM apuesta WHERE player_id = player AND game_id = game);
	
	-- Sumando valor apostado al saldo del jugador 
	UPDATE jugador SET balance = balance + quantity WHERE player_id = player; 
	
	-- Eliminando registro de la apuesta
	DELETE FROM apuesta WHERE player_id = player AND game_id = game; 
	
	-- Restando valor apostado a apuesta total del juego
	UPDATE juegos SET total_bet = total_bet - quantity WHERE game_id = game;
	
	
	-- Registrando transacción en OLAP 
	INSERT INTO hechos_transacciones (player_id, game_id, cantidad, tipo_transaccion, tiempo_id)
    VALUES (
        (SELECT dim_jugador_id FROM "Dim_Jugador" WHERE player_id = player AND fecha_fin IS NULL LIMIT 1), 
		(SELECT dim_juego_id FROM "Dim_Juego" WHERE game_id = game AND fecha_fin IS NULL LIMIT 1),
        quantity, 
        'Cancelación apuesta', 
        (SELECT dim_tiempo_id FROM "Dim_Tiempo" WHERE fecha = CURRENT_DATE LIMIT 1)
    ); 

	RETURN; 
END;
$$ LANGUAGE plpgsql;