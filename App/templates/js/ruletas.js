//Lista de opciones de la Ruleta
var options = ["0", "32", "15", "19", "4", "21", "2", "25", "17", "34", "6", "27", "13", "36", "11", "30", "8", "23", "10", "5", "24", "16", "33", "1", "20", "14", "31", "9", "22", "18", "29", "7", "28", "12", "35", "3", "26"];
//variables para posicionar el lugar de cada numero
var startAngle = 0;
var arc = Math.PI / (options.length / 2);
//Variables de tiempo de giro
var spinTimeout = null;
var spinTime = 0;
var spinTimeTotal = 0;
//canva
var ctx;
//Valor objetivo
var targetValue = "0";
var targetIndex = options.indexOf(targetValue);
//Aleatorios Giro, tiempo de giro y angulo de precision
var ranGiro = Math.ceil(Math.random() * (6 - 3)) + 3;
var ranAngle = Math.ceil(Math.random() * (9 - 1)) + 1;
var ranSpin = Math.ceil(Math.random() * (10000 - 5000)) + 5000;

const button = document.getElementById('spin')

//Funcion para determinar el target value 
function searchResult(){
    fetch("{{ url_for('result', id = id) }}")
    .then(res => {
        return res.json()
    })
    .then((response) => {
        if (response["value"] != "-1") {
            targetValue = response["value"];
            targetIndex = options.indexOf(targetValue);
            button.style.display = 'None'; 
            spin();
            
        }
        else {
            button.innerText = 'No hay resultado aún'; 
            setTimeout(()=>{
                button.innerText = 'Spin the Wheel!'; 
            }, 4000)
        }
    })
}


button.addEventListener("click", searchResult)


//Funcion que elige los colores de cada casilla
function getColor(item, maxitem) {
    const redNumbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36];
    const blackNumbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35];
    if (item == 0) {
        return "#27933e"; // Verde para el 0
    }
    if (redNumbers.includes(parseInt(options[item]))) {
        return "#b43b3d"; // Rojo
    }
    if (blackNumbers.includes(parseInt(options[item]))) {
        return "#2a2c3f"; // Negro
    }
    return "#FFFFFF";
}

//Funcion que dibuja la ruleta
function drawRouletteWheel() {
    var canvas = document.getElementById("canvas");

    if (canvas.getContext) {
        var outsideRadius = 250; //Radio del circulo externo
        var textRadius = 220; //Ubicacion de los numeros
        var insideRadius = 125; //Radio del circulo menor
        var mediumRadius = 175; //Radio del circulo del medio
        //Estilo del canvas
        ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, 500, 500);
        ctx.strokeStyle = "black";
        ctx.lineWidth = 3;
        ctx.font = 'bold 12px Helvetica, Arial';
        //Dibuja los circulos, sus particiones y ubica el texto
        for (var i = 0; i < options.length; i++) {
            var angle = startAngle + i * arc;
            ctx.fillStyle = getColor(i, options.length);
            ctx.beginPath();
            ctx.arc(250, 250, outsideRadius, angle, angle + arc, false);
            ctx.arc(250, 250, insideRadius, angle + arc, angle, false);
            ctx.arc(250, 250, mediumRadius, angle + arc, angle, true);
            ctx.stroke();
            ctx.fill();
            ctx.save();
            ctx.fillStyle = "white";
            ctx.translate(250 + Math.cos(angle + arc / 2) * textRadius,
                          250 + Math.sin(angle + arc / 2) * textRadius);
            ctx.rotate(angle + arc / 2 + Math.PI / 2);
            var text = options[i];
            ctx.fillText(text, -ctx.measureText(text).width / 2, 0);
            ctx.restore();
        }

        // Flecha
        ctx.fillStyle = "white";
        ctx.beginPath();
        ctx.moveTo(250 + (outsideRadius + 10), 250 + 8);
        ctx.lineTo(250 + (outsideRadius + 10), 250 - 8);
        ctx.lineTo(250 + (outsideRadius - 15), 250);
        ctx.fill();
    }
}

//funcion que lleva cuenta del tiempo de giro
function spin() {
    spinTime = 0;
    spinTimeTotal = ranSpin; // Tiempo de giro aleatorio entre 6 y 10 segundos
    rotateWheel();
}
//Funcion que hace desacelerar el giro al final
function easeOut(t, b, c, d) {
    var ts = (t/=d)*t;
    var tc = ts*t;
    return b+c*(tc + -3*ts + 3*t);
}

//Funcion que hace girar la rueda
function rotateWheel() {
    spinTime += 15;
    if (spinTime >= spinTimeTotal) {
        stopRotateWheel();
        return;
    }
    //Registros de pocision del valor objetivo 
    var targetAngle = (360 - (targetIndex * (arc * 180 / Math.PI))) % 360; //Angulo del valor objetivo
    var totalRotations = ranGiro * 360; //Cantidad de giros que da
    var progress = spinTime / spinTimeTotal; //Mide la razon de del tiempo transcurrido
    var easedProgress = easeOut(spinTime, 0, 1, spinTimeTotal); //llama la funcion easeout para el momento actual
    var totalAngleToRotate = totalRotations + targetAngle; //Cantidad de recorrido
    var currentRotation = totalAngleToRotate * (1 - easedProgress) - targetAngle + ranAngle; //Cantidad de rotaciones actuales

    startAngle = -(currentRotation * Math.PI / 180);//Actualiza el angulo desde el que se comienza a dibujar
    drawRouletteWheel();
    spinTimeout = setTimeout(rotateWheel, 30);
    
}

//Funcion que detiene el giro de la rueda
function stopRotateWheel() {
    clearTimeout(spinTimeout);
    document.getElementById("result-text").innerText = options[targetIndex];
    ranGiro = Math.ceil(Math.random() * (6 - 3)) + 3; //Seleccion de un numero entre 3 y 6 para que gire la rueda
    ranAngle = Math.ceil(Math.random() * (9 - 1)) + 1; //Seleccion de un numero entre  1 y 9 como angulo de fallo para el valor objetivo 
    ranSpin = Math.ceil(Math.random() * (10000 - 5000)) + 5000; //Seleccion de un numero entre 10s y 1s como tioempo para que gire la ruleta
    
}


drawRouletteWheel();