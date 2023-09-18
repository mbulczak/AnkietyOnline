const paramsSurveyAddChoiceItem = document.currentScript.dataset;

$(document).ready(function() {
    let wyboryFormset = $('#choice-wrapper');
    let addButton = $('#add-choice');
    let totalForms = parseInt(paramsSurveyAddChoiceItem.totalFormCount);
    let removeBtnHtml= `<button type="button" class="btn btn-danger btn-sm remove-choice">Usuń</button>`;
    let emptyFormset = $('#choice-empty-form');

    addButton.click(function() {
        let newForm = emptyFormset.clone(true);

        newForm.removeAttr("id");
        newForm.removeClass("d-none");
        newForm.addClass("choice");
        txt = newForm.html();
        newForm.html(txt.replaceAll("__prefix__", totalForms));
        newForm.append(removeBtnHtml);
        newForm.insertAfter('.choice:last');
        totalForms++;
        $("#id_choice_set-TOTAL_FORMS").val(totalForms);
    });

    wyboryFormset.on('click', '.remove-choice', function() {
        $(this).closest('.choice').remove();
    });

    toggleChoiseWrapper();
    $("#id_type").on("change", function() {
        toggleChoiseWrapper();
    });
});

function toggleChoiseWrapper() {
    wrapper = $('#choice-wrapper');
    possibleTypes = ["choice", "multiple_choice"];
    questionType = $('#id_type');
    questionTypeValue = questionType.find(":selected").val();

    if(possibleTypes.includes(questionTypeValue)) {
        wrapper.show();
    }
    else {
        wrapper.hide();
    }
}
