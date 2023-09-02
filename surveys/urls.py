from django.urls import path
from . import views
from . import ajax

app_name = "surveys"

urlpatterns = [
    path("my-surveys/", views.user_surveys, name="user_surveys"),
    path("create-survey/", views.create_survey, name="create_survey"),
    path("edit-survey/<int:survey_id>/", views.edit_survey, name="edit_survey"),
    path("delete-survey/<int:survey_id>/", views.delete_survey, name="delete_survey"),
    path("add-question/<int:survey_id>/", views.add_question, name="add_question"),
    path("delete-question/<int:question_id>/", views.delete_question, name="delete_question"),
    path("edit-question/<int:question_id>/", views.edit_question, name="edit_question"),
    path("survey-questions/<int:survey_id>/", views.survey_questions, name="survey_questions"),
    path("<int:survey_id>/fill/", views.fill_survey, name="fill_survey"),
    path("filled/<int:response_id>/", views.survey_filled, name="survey_filled"),
    path("share/<int:survey_id>/", views.share_survey, name="share_survey"),
    path("qr/<int:survey_id>/", views.qr_code, name="qr_code"),
    path("survey/<int:survey_id>/statistics/", views.survey_statistics, name="survey_statistics"),
    path("delete-all-answers/<int:survey_id>", views.delete_all_answers, name="delete_all_answers"),

    path("update-question-position/", ajax.update_question_position, name="update_question_position"),
]
