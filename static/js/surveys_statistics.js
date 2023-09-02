$(document).ready(function() {
    $(".survey-question-chart").each(function(i, e) {
        console.log($(e).data());

        chartLabels = eval($(e).data("questionLables"));
        chartValues = $(e).data("questionValues");

        var myChart = new Chart(e, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: "Liczba odpowiedzi",
                data: chartValues,
            }]
        }
        });
    });
});