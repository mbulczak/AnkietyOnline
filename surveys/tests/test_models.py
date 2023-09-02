from django.test import TestCase
from users.models import User
from surveys.models import Survey, Question, Choice, Response, Answer


class SurveyModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(
            title="Przykładowa ankieta",
            description="To jest przykładowa ankieta",
            created_by=self.user
        )

    def test_survey_creation(self):
        survey = self.survey
        self.assertEqual(survey.title, "Przykładowa ankieta")
        self.assertEqual(survey.description, "To jest przykładowa ankieta")
        self.assertTrue(survey.is_active)
        self.assertEqual(survey.created_by, self.user)
        self.assertTrue(survey.created_at)
        self.assertTrue(survey.modified_at)

    def test_survey_str_representation(self):
        survey_str = str(self.survey)
        self.assertEqual(survey_str, "Przykładowa ankieta")


class QuestionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(
            title="Przykładowa ankieta",
            created_by=self.user
        )
        self.question = Question.objects.create(
            survey=self.survey,
            title="Przykładowe pytanie",
            type=Question.TEXT,
            ordinal_number=1
        )

    def test_question_creation(self):
        question = self.question
        self.assertEqual(question.survey, self.survey)
        self.assertEqual(question.title, "Przykładowe pytanie")
        self.assertEqual(question.type, Question.TEXT)
        self.assertEqual(question.ordinal_number, 1)

    def test_question_str_representation(self):
        question_str = str(self.question)
        self.assertEqual(question_str, "Przykładowe pytanie")

    def test_question_unique_together(self):
        with self.assertRaises(Exception):
            Question.objects.create(
                survey=self.survey,
                title="Kolejne przykładowe pytanie",
                type=Question.TEXT,
                ordinal_number=1
            )


class ChoiceModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(
            title="Przykładowa ankieta",
            created_by=self.user
        )
        self.question = Question.objects.create(
            survey=self.survey,
            title="Przykładowe pytanie",
            type=Question.CHOICE,
            ordinal_number=1
        )
        self.choice = Choice.objects.create(
            question=self.question,
            text="Przykładowy wybór",
            ordinal_number=1
        )

    def test_choice_creation(self):
        choice = self.choice
        self.assertEqual(choice.question, self.question)
        self.assertEqual(choice.text, "Przykładowy wybór")
        self.assertEqual(choice.ordinal_number, 1)

    def test_choice_str_representation(self):
        choice_str = str(self.choice)
        self.assertEqual(choice_str, "Przykładowy wybór")

    def test_choice_unique_together(self):
        with self.assertRaises(Exception):
            Choice.objects.create(
                question=self.question,
                text="Kolejny przykładowy wybór",
                ordinal_number=1
            )


class ResponseModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(
            title="Przykładowa ankieta",
            created_by=self.user
        )
        self.response = Response.objects.create(
            survey=self.survey,
            respondent_user=self.user
        )

    def test_response_creation(self):
        response = self.response
        self.assertEqual(response.survey, self.survey)
        self.assertEqual(response.respondent_user, self.user)
        self.assertTrue(response.submitted_at)

    def test_response_str_representation(self):
        response_str = str(self.response)
        expected_str = f"{self.survey.title} - {self.response.respondent_user}"
        self.assertEqual(response_str, expected_str)


class AnswerModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.survey = Survey.objects.create(
            title="Przykładowa ankieta",
            created_by=self.user
        )
        self.question = Question.objects.create(
            survey=self.survey,
            title="Przykładowe pytanie",
            type=Question.TEXT,
            ordinal_number=1
        )
        self.response = Response.objects.create(
            survey=self.survey,
            respondent_user=self.user
        )
        self.answer = Answer.objects.create(
            question=self.question,
            response=self.response,
            answer_text="Przykładowa odpowiedź"
        )

    def test_answer_creation_text_question(self):
        answer = self.answer 
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.response, self.response)
        self.assertEqual(answer.answer_text, "Przykładowa odpowiedź")
        self.assertIsNone(answer.chosen_choice)

    def test_answer_creation_choice_question(self):
        self.question.type = Question.CHOICE
        self.question.save()
        choice = Choice.objects.create(
            question=self.question,
            text="Przykładowy wybór",
            ordinal_number=1
        )
        answer = Answer.objects.create(
            question=self.question,
            response=self.response,
            chosen_choice=choice
        )
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.response, self.response)
        self.assertIsNone(answer.answer_text)
        self.assertEqual(answer.chosen_choice, choice)

    def test_answer_str_representation_text_question(self):
        answer_str = str(self.answer)
        expected_str = f"{self.question.title} - {self.answer.answer_text}"
        self.assertEqual(answer_str, expected_str)

    def test_answer_str_representation_choice_question(self):
        self.question.type = Question.CHOICE
        self.question.save()
        choice = Choice.objects.create(
            question=self.question,
            text="Przykładowy wybór",
            ordinal_number=1
        )
        answer = Answer.objects.create(
            question=self.question,
            response=self.response,
            chosen_choice=choice
        )
        answer_str = str(answer)
        expected_str = f"{self.question.title} - {choice.text}"
        self.assertEqual(answer_str, expected_str)
