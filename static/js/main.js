function drawChart(params) {
    cosnole.log(params);
    // Dane do wykresu
    var data = {
        labels: params.labels,
        datasets: [{
            data: params.data,
        }]
    };

    // Opcje wykresu
    var options = {
        responsive: true,
        maintainAspectRatio: false
    };

    // Pobierz element canvas
    var ctx = document.getElementById('myPieChart').getContext('2d');

    // Tworzenie wykresu kołowego
    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });
}