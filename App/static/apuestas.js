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