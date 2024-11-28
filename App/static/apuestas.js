// Seleccionar el input de la apuesta
const betAmountInput = document.getElementById('betAmount');

// Seleccionar los botones
const addButtons = document.querySelectorAll('.bet-input button[data-amount]');
const halfButton = document.getElementById('half');
const doubleButton = document.getElementById('double');
const maxButton = document.getElementById('max');
const clearButton = document.getElementById('clear');

// Función para actualizar la apuesta
function updateBetAmount(value) {
  let currentBet = parseFloat(betAmountInput.value);
  if (isNaN(currentBet)) {
    currentBet = 0;
  }
  betAmountInput.value = currentBet + value;
}

// Función para dividir la apuesta entre 2
halfButton.addEventListener('click', () => {
  let currentBet = parseFloat(betAmountInput.value);
  if (!isNaN(currentBet) && currentBet >= 1) {
    let halfBet = Math.floor(currentBet / 2); 
    if (halfBet >= 1) {
      betAmountInput.value = halfBet;
    }
  }
});

// Función para multiplicar la apuesta por 2
doubleButton.addEventListener('click', () => {
  let currentBet = parseFloat(betAmountInput.value);
  if (!isNaN(currentBet) && currentBet > 0) {
    betAmountInput.value = currentBet * 2;
  }
});

// Función para poner el valor máximo
maxButton.addEventListener('click', () => {
  betAmountInput.value = 9999;
});

//Función para poner el valor en 0
clearButton.addEventListener('click', () => {
    betAmountInput.value = 0;
  });
// Agregar evento a los botones de sumar
addButtons.forEach(button => {
  button.addEventListener('click', () => {
    const amount = parseFloat(button.getAttribute('data-amount'));
    updateBetAmount(amount);
  });
});

// Controlador de la barra de apuestas

// Seleccionar las tarjetas de apuesta
const betCards = document.querySelectorAll('.bet-card');

// Seleccionar el modal y los elementos de confirmación
const modal = document.getElementById('betConfirmationModal');
const betColorSpan = document.getElementById('betColor');
const confirmButton = document.getElementById('confirmBet');
const cancelButton = document.getElementById('cancelBet');

// Variable para almacenar la tarjeta seleccionada
let selectedCard = null;

// Agregar un evento de clic a cada tarjeta
betCards.forEach(card => {
  card.addEventListener('click', function() {
    // Si ya está seleccionada, no hacer nada
    if (this.classList.contains('selected')) return;

    // Obtener el color de la apuesta y actualizar el texto
    let color, colorName; 
    if (this.classList.contains('red')) {
      color = '#D32F2F'; // Rojo
      colorName = 'Rojo';
    } else if (this.classList.contains('green')) {
      color = '#5dbb2f'; // Verde
      colorName = 'Verde';
    } else {
      color = '#000000'; // Gris
      colorName = 'Negro';
    }

    // Mostrar el modal con el mensaje de confirmación
    betColorSpan.textContent = colorName; // Mostrar el color y nombre en el mensaje
    betColorSpan.style.color = color; // Cambiar el color del texto
    modal.style.display = 'flex'; // Mostrar el modal
    selectedCard = this; // Guardar la tarjeta seleccionada
  });
});

// Función para confirmar la apuesta
confirmButton.addEventListener('click', function() {
  // Marcar la tarjeta como seleccionada y oscurecerla
  betCards.forEach(card => card.classList.remove('selected'));
  selectedCard.classList.add('selected');

  // Cerrar el modal
  modal.style.display = 'none';
});

// Función para cancelar la apuesta
cancelButton.addEventListener('click', function() {
  // Cerrar el modal sin hacer cambios
  modal.style.display = 'none';
});

// Función para hacer el calculo de la ganancia potencial

// Multiplicadores para cada color
const betMultipliers = {
  red: 2,     // Ejemplo: 2x para rojo
  green: 36,  // Ejemplo: 36x para verde
  black: 2    // Ejemplo: 2x para negro
};

// Función para actualizar la ganancia potencial en todas las tarjetas
function updatePotentialProfit() {
  const currentBet = parseFloat(betAmountInput.value);

  // Si hay una apuesta válida
  if (!isNaN(currentBet) && currentBet > 0) {
    // Actualizar la ganancia potencial en cada tarjeta
    betCards.forEach(card => {
      const betType = card.dataset.bet; // Obtener el tipo de apuesta (red, green, black)
      const multiplier = betMultipliers[betType] || 1; // Obtener el multiplicador correspondiente
      const potentialProfit = currentBet * multiplier; // Calcular la ganancia potencial

      // Actualizar el texto dentro de la tarjeta
      card.querySelector('.profit').textContent = `Ganancia potencial: $${potentialProfit.toFixed(2)}`;
    });
  } else {
    // Si no hay una apuesta válida, limpiar el texto en todas las tarjetas
    betCards.forEach(card => {
      card.querySelector('.profit').textContent = 'Ganancia potencial: $0.00';
    });
  }
}

// Función auxiliar para actualizar el valor del input
function setBetAmount(value) {
  betAmountInput.value = value;
  // Disparar actualización de ganancias cada vez que cambia el valor
  updatePotentialProfit();
}

// Evento para actualizar la ganancia cuando cambia manualmente el valor del input
betAmountInput.addEventListener('input', updatePotentialProfit);

// Actualizar ganancia cuando se presionan los botones
addButtons.forEach(button => {
  button.addEventListener('click', () => {
    const currentBet = parseFloat(betAmountInput.value) || 0;
    setBetAmount(currentBet);
  });
});

halfButton.addEventListener('click', () => {
  const currentBet = parseFloat(betAmountInput.value) || 0;
  setBetAmount(currentBet); // Al menos 1 si es válido
});

doubleButton.addEventListener('click', () => {
  const currentBet = parseFloat(betAmountInput.value) || 0;
  setBetAmount(currentBet);
});

maxButton.addEventListener('click', () => {
  const currentBet = parseFloat(betAmountInput.value) || 0;
  setBetAmount(currentBet); // Valor máximo
});

clearButton.addEventListener('click', () => {
  const currentBet = parseFloat(betAmountInput.value) || 0;
  setBetAmount(currentBet); // Valor máximo
});

// Seleccionar el botón de aceptar apuesta
const acceptBetButton = document.getElementById('confirmBet');

// Función para manejar la aceptación de la apuesta
function submitBet() {
  // Obtener el monto de la apuesta
  const betAmount = parseFloat(betAmountInput.value);

  // Validar el monto
  if (isNaN(betAmount) || betAmount <= 0) {
    alert("Por favor, ingresa un monto válido para la apuesta.");
    return;
  }

  // Obtener el color seleccionado
  const selectedColorCard = document.querySelector('.bet-card.selected');
  if (!selectedColorCard) {
    alert("Por favor, selecciona un color para apostar.");
    return;
  }

  const betColor = selectedColorCard.dataset.bet; // Ejemplo: 'red', 'green', 'black'

  // Realizar acciones con la apuesta
  console.log(`Apuesta confirmada: ${betAmount} al color ${betColor}`);
  alert(`Apuesta realizada: $${betAmount} al color ${betColor}. ¡Buena suerte!`);

  // Puedes realizar una solicitud a un servidor aquí o ejecutar otra lógica
  // Por ejemplo:
  // sendBetToServer({ amount: betAmount, color: betColor });

  // Reiniciar valores después de confirmar
  betAmountInput.value = '';
  selectedCard.classList.remove('selected');
  updatePotentialProfit(); // Actualizar las ganancias potenciales
}

// Vincular la función al botón de aceptar
acceptBetButton.addEventListener('click', submitBet);

