const paramsSurveyQuestions = document.currentScript.dataset;

$(document).ready(function() {
    $(".sortable-icon-up").on("click", function() {
        qTile = $(this).parent().parent();

        if (qTile.prev(".question-tile").length) {
            qTile.insertBefore(qTile.prev());
            updateNumbers();
            updateNumbersDjango();
        }
    });

    $(".sortable-icon-down").on("click", function() {
        qTile = $(this).parent().parent();

        if (qTile.next(".question-tile").length) {
            qTile.insertAfter(qTile.next());
            updateNumbers();
            updateNumbersDjango();
        }
    });
});

function updateNumbers() {
    $(".question-tile").each(function(index) {
        $(this).find(".ordinal-number").text(index + 1);
    });
}

function updateNumbersDjango() {
    var newOrder = [];

    $(".question-tile").each(function() {
        newOrder.push($(this).data("id"));
    });

    $.ajax({
        type: "POST",
        url: paramsSurveyQuestions.url,
        data: {
            "csrfmiddlewaretoken": paramsSurveyQuestions.csrfmiddlewaretoken,
            'order[]': newOrder
        },
        success: function(response) {
            console.log("Pozycja zapisana.");
        },
        error: function(response) {
            console.error("Błąd podczas zapisu.");
            console.error(response);
        }
    });
}