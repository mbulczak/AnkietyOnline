from django.test import TestCase
from django.urls import reverse, resolve
from surveys import views, ajax

class SurveyURLsTestCase(TestCase):
    sample_survey_id = 1
    sample_question_id = 2
    sample_response_id = 3

    def test_user_surveys_url(self):
        url = reverse("surveys:user_surveys")
        self.assertEqual(resolve(url).func, views.user_surveys)

    def test_create_survey_url(self):
        url = reverse("surveys:create_survey")
        self.assertEqual(resolve(url).func, views.create_survey)

    def test_edit_survey_url(self):
        url = reverse("surveys:edit_survey", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.edit_survey)

    def test_delete_survey_url(self):
        url = reverse("surveys:delete_survey", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.delete_survey)

    def test_add_question_url(self):
        url = reverse("surveys:add_question", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.add_question)

    def test_delete_question_url(self):
        url = reverse("surveys:delete_question", args=[self.sample_question_id])
        self.assertEqual(resolve(url).func, views.delete_question)

    def test_edit_question_url(self):
        url = reverse("surveys:edit_question", args=[self.sample_question_id])
        self.assertEqual(resolve(url).func, views.edit_question)

    def test_survey_questions_url(self):
        url = reverse("surveys:survey_questions", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.survey_questions)

    def test_fill_survey_url(self):
        url = reverse("surveys:fill_survey", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.fill_survey)

    def test_survey_filled_url(self):
        url = reverse("surveys:survey_filled", args=[self.sample_response_id])
        self.assertEqual(resolve(url).func, views.survey_filled)

    def test_share_survey_url(self):
        url = reverse("surveys:share_survey", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.share_survey)

    def test_qr_code_url(self):
        url = reverse("surveys:qr_code", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.qr_code)

    def test_survey_statistics_url(self):
        url = reverse("surveys:survey_statistics", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.survey_statistics)

    def test_delete_all_answers_url(self):
        url = reverse("surveys:delete_all_answers", args=[self.sample_survey_id])
        self.assertEqual(resolve(url).func, views.delete_all_answers)

    def test_update_question_position_url(self):
        url = reverse("surveys:update_question_position")
        self.assertEqual(resolve(url).func, ajax.update_question_position)
