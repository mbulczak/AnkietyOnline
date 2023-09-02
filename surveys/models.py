from django.db import models 
from users.models import User


class Survey(models.Model):
    title = models.CharField(verbose_name="Tytuł", max_length=256)
    description = models.TextField(verbose_name="Opis", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktywna")
    modified_at = models.DateTimeField(auto_now=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


class Question(models.Model):
    TEXT = "text"
    CHOICE = "choice"
    MULTIPLE_CHOICE = "multiple_choice"
    
    QUESTION_TYPES = [
        (TEXT, "Pytanie otwarte"),
        (CHOICE, "Pytanie jednokrotnego wyboru"),
        (MULTIPLE_CHOICE, "Pytanie wielokrotnego wyboru"),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name="Tytuł")
    desctiption = models.TextField(verbose_name="Opis", blank=True)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="Typ")
    ordinal_number = models.IntegerField(default=1)

    class Meta:
        unique_together = ["survey", "ordinal_number"]
    
    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, verbose_name="Tekst")
    ordinal_number = models.IntegerField(default=1)

    class Meta:
        unique_together = ["question", "ordinal_number"]
    
    def __str__(self):
        return self.text


class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    respondent_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.survey.title} - {self.respondent_user}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE, default=None)
    answer_text = models.TextField(blank=True, null=True)
    chosen_choice = models.ForeignKey(Choice, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        if self.chosen_choice:
            return f"{self.question.title} - {self.chosen_choice.text}"
        else:
            return f"{self.question.title} - {self.answer_text}"
