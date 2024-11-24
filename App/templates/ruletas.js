var options = ["0", "32", "15", "19", "4", "21", "2", "25", "17", "34", "6", "27", "13", "36", "11", "30", "8", "23", "10", "5", "24", "16", "33", "1", "20", "14", "31", "9", "22", "18", "29", "7", "28", "12", "35", "3", "26"];
var startAngle = 0;
var arc = Math.PI / (options.length / 2);
var spinTimeout = null;
var spinTime = 0;
var spinTimeTotal = 0;
var ctx;
var targetValue = "32";
var targetIndex = options.indexOf(targetValue);

document.getElementById("spin").addEventListener("click", spin);

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

function drawRouletteWheel() {
    var canvas = document.getElementById("canvas");
    if (canvas.getContext) {
        var outsideRadius = 250;
        var textRadius = 220;
        var insideRadius = 125;
        var mediumRadius = 175;
        ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, 500, 500);
        ctx.strokeStyle = "black";
        ctx.lineWidth = 3;
        ctx.font = 'bold 12px Helvetica, Arial';

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

function spin() {
    spinTime = 0;
    spinTimeTotal = 5000; // Aumentamos el tiempo total a 5 segundos
    rotateWheel();
}

function easeOut(t, b, c, d) {
    var ts = (t/=d)*t;
    var tc = ts*t;
    return b+c*(tc + -3*ts + 3*t);
}

function rotateWheel() {
    spinTime += 15;
    if (spinTime >= spinTimeTotal) {
        stopRotateWheel();
        return;
    }
     
    var targetAngle = (360 - (targetIndex * (arc * 180 / Math.PI))) % 360;
    var totalRotations = 8 * 360;
    var progress = spinTime / spinTimeTotal;
    var easedProgress = easeOut(spinTime, 0, 1, spinTimeTotal);
    var totalAngleToRotate = totalRotations + targetAngle;
    var currentRotation = totalAngleToRotate * (1 - easedProgress) + 15.2;

    startAngle = -(currentRotation * Math.PI / 180);
    drawRouletteWheel();
    spinTimeout = setTimeout(rotateWheel, 30);
    
}

function stopRotateWheel() {
    clearTimeout(spinTimeout);
    document.getElementById("result-text").innerText = options[targetIndex];
}

drawRouletteWheel();