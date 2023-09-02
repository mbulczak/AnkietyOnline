from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Survey, Question, Choice, Response, Answer
from .forms import SurveyForm, QuestionForm, ChoiceForm, ChoiceFormSet, ResponseForm
from django.db.models import Max
import qrcode
from io import BytesIO


@login_required
def user_surveys(request):
    surveys = Survey.objects.filter(created_by=request.user).order_by("-is_active", "-modified_at")

    return render(request, "surveys/user_surveys.html", {
        "surveys": surveys
    })


@login_required
def create_survey(request):
    if request.method == "POST":
        form = SurveyForm(request.POST)
        
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.save()

            messages.success(request, f"Utworzono ankietę { survey.title }")

            return redirect("surveys:survey_questions", survey.id)
    else:
        form = SurveyForm()
    return render(request, "surveys/create_survey.html", {
        "form": form
    })


@login_required
def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == "POST":
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()

            messages.success(request, "Zapisano")
            return redirect("surveys:user_surveys")
    else:
        form = SurveyForm(instance=survey)

    return render(request, "surveys/edit_survey.html", {
        "form": form,
        "survey": survey
    })


@login_required
def survey_questions(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == "POST":
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()

            messages.success(request, "Zapisano")
            return redirect("surveys:user_surveys")
    else:
        form = SurveyForm(instance=survey)
        form_questions = QuestionForm()

    return render(request, "surveys/survey_questions.html", {
        "form": form,
        "form_questions": form_questions,
        "survey": survey
    })



@login_required
def delete_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, created_by=request.user)

    survey.delete()

    messages.success(request, f"Usunięto ankietę {survey.title}")
    return redirect("surveys:user_surveys") 


@login_required
def add_question(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, created_by=request.user)
    questions = Question.objects.filter(survey_id=survey_id)
    questions_max_ordinal_number = questions.aggregate(Max("ordinal_number"))

    if request.method == "POST":
        print(request.POST)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            choice_formset = ChoiceFormSet(request.POST, instance=question)
            
            if choice_formset.is_valid():
                for i, form in enumerate(choice_formset, start=1):
                    choice = form.save(commit=False)
                    choice.ordinal_number = i
                    choice.question = question

                question.save()
                choice_formset.save()

                messages.success(request, "Utworzono pytanie")
            else:
                question.save()
                messages.success(request, f"Zapisano bez pytania")


            return redirect("surveys:survey_questions", survey_id)
    else:
        form = QuestionForm()
        print(questions_max_ordinal_number)
        if questions_max_ordinal_number["ordinal_number__max"]:
            form.fields["ordinal_number"].initial = questions_max_ordinal_number["ordinal_number__max"] + 1
        else:
            form.fields["ordinal_number"].initial = 1

        choice_formset = ChoiceFormSet()
    return render(request, "surveys/add_question.html", {
        "form": form,
        "survey": survey,
        "choice_formset": choice_formset
    })


@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    choices = Choice.objects.filter(question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        choice_formset = ChoiceFormSet(request.POST, instance=question)

        if form.is_valid():
            form.save()
        
        if choice_formset.is_valid():
            for i, form in enumerate(choice_formset, start=1):
                choice = form.save(commit=False)
                choice.ordinal_number = i
                choice.question = question
        
            choice_formset.save()

        messages.success(request, "Zapisano")
        return redirect("surveys:survey_questions", question.survey.id) 
    else:
        form = QuestionForm(instance=question)
        choice_formset = ChoiceFormSet(instance=question)
        choice_formset.extra = 0

    return render(request, "surveys/edit_question.html", {
        "form": form,
        "choice_formset": choice_formset,
        "question": question,
        "survey": question.survey
    })


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()

    change_question_order(request, question.survey_id)

    messages.success(request, f"Usunięto pytanie \"{question.title}\"")

    return redirect("surveys:survey_questions", question.survey.id)


def change_question_order(request, survey_id):
    question_ids = Question.objects.filter(survey_id=survey_id)
    ordered_questions = question_ids.order_by("ordinal_number")

    for index, question in enumerate(ordered_questions, start=1):
        question.ordinal_number = index
        question.save()

    messages.success(request, "Posortowano pytania")


def fill_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, is_active=True)

    if request.method == "POST":
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            return redirect("surveys:survey_filled", response_id=response.id)
    else:
        form = ResponseForm(survey=survey)

    return render(request, "surveys/fill_survey.html", {"form": form, "survey": survey})


def survey_filled(request, response_id):
    response = get_object_or_404(Response, pk=response_id)
    return render(request, "surveys/survey_filled.html", {"response": response})


def share_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    return render(request, "surveys/share_survey.html", {
        "survey": survey,
    })


def qr_code(request, survey_id):
    abs_url = request.build_absolute_uri(reverse("surveys:fill_survey", args=[survey_id]))
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(abs_url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    img_stream = BytesIO()
    qr_img.save(img_stream, format="PNG")
    
    response = HttpResponse(content_type="image/png")
    response.write(img_stream.getvalue())
    
    return response


def survey_statistics(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, created_by=request.user)
    questions = survey.question_set.all().order_by("ordinal_number")
    questions_total_responses = Response.objects.filter(survey=survey).count()
    question_statistics = []

    for question in questions:
        statistics = {}
        statistics["question"] = question
        statistics["chart"] = {}
        statistics["chart"]["labels"] = []
        statistics["chart"]["values"] = []

        statistics["answers"] = Answer.objects.filter(response__survey=survey, question=question)

        if question.type != Question.TEXT:
            statistics["choices"] = question.choice_set.all()
            choice_counts = []
            for choice in statistics["choices"]:
                count = Answer.objects.filter(response__survey=survey, question=question, chosen_choice=choice).count()
                choice_counts.append((choice, count))
            statistics["choice_counts"] = choice_counts
            
            for choice, count in choice_counts:
                statistics["chart"]["labels"].append(choice.text)
                statistics["chart"]["values"].append(count)

        question_statistics.append(statistics)

    return render(request, "surveys/survey_statistics.html", {
        "survey": survey, 
        "question_statistics": question_statistics,
        "questions_total_responses": questions_total_responses,
    })


def delete_all_answers(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, created_by=request.user)
    res = Response.objects.filter(survey=survey)
    res.delete()

    messages.success(request, "Usunięto wszystkie odpowiedzi")

    return redirect("surveys:survey_statistics", survey.id)
