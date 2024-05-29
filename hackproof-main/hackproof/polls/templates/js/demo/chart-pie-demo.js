function criarGrafico() {
  // Exemplo de Gráfico de Pizza
  var ctx = document.getElementById("myPieChart");
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Acesso Autorizado", "Origem Desconhecida", "Acesso Não Autorizado"],
      datasets: [{
        data: [obterValorAlto(), 13, 10], // Ajustando os valores
        backgroundColor: ['#1cc88a', '#f6c23e', '#e74a3b'], // Ajustando as cores
        hoverBackgroundColor: ['#17a673', '#f3b418', '#c0392b'], // Ajustando as cores do hover
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }]
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10
      },
      legend: {
        display: false
      },
      cutoutPercentage: 80
    }
  });

  // Função para obter valores aleatórios entre 75 e 100 para dar mais ênfase a "Acesso Autorizado" (alto)
  function obterValorAlto() {
    return Math.floor(Math.random() * 26) + 75;
  }
}

// Chamando a função para criar o gráfico
criarGrafico();
