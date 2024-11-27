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
