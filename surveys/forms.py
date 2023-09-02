from django import forms
from .models import Survey, Question, Choice, Response, Answer


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["title", "description", "is_active"]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 3
                }
            )
        }


class QuestionForm(forms.ModelForm):
    ordinal_number = forms.IntegerField(widget=forms.HiddenInput()) 

    class Meta:
        model = Question
        fields = ["title", "type", "ordinal_number"]


class ChoiceForm(forms.ModelForm):
    ordinal_number = forms.IntegerField(widget=forms.HiddenInput()) 

    class Meta:
        model = Choice
        fields = ["text", "ordinal_number"]


ChoiceFormSet = forms.inlineformset_factory(
    Question,
    Choice, fields=["text"], 
    extra=1, 
    can_delete=True, 
    can_delete_extra=False, 
    min_num=1,
    widgets={
        "text": forms.TextInput()
    }, 
)


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = []

    def __init__(self, *args, survey=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        for question in self.survey.question_set.all().order_by("ordinal_number"):
            field_name = f"question_{question.id}"
            question_label = f"{question.ordinal_number}. {question.title}"

            if question.type == Question.TEXT:
                self.fields[field_name] = forms.CharField(
                    label=question_label,
                    widget=forms.Textarea(attrs={"rows": 4, "cols": 50})
                )
            elif question.type == Question.CHOICE:
                self.fields[field_name] = forms.ModelChoiceField(
                    label=question_label,
                    help_text="Można udzielić jednej odpowiedzi.",
                    queryset=question.choice_set.all(),
                    widget=forms.RadioSelect
                )
            elif question.type == Question.MULTIPLE_CHOICE:
                self.fields[field_name] = forms.ModelMultipleChoiceField(
                    label=question_label,
                    help_text="Można zaznaczyć kilka odpowiedzi.",
                    queryset=question.choice_set.all(),
                    widget=forms.CheckboxSelectMultiple
                )

    def save(self):
        response = super().save(commit=False)
        response.survey = self.survey

        if self.user.is_authenticated:
            response.respondent_user = self.user.username
            
        response.save()

        for question in self.survey.question_set.all():
            field_name = f"question_{question.id}"
            answer_data = self.cleaned_data[field_name]

            if question.type == Question.TEXT:
                Answer.objects.create(
                    response=response,
                    question=question,
                    answer_text=answer_data
                )
            elif question.type == Question.CHOICE:
                Answer.objects.create(
                    response=response,
                    question=question,
                    chosen_choice=answer_data
                )
            else:
                for choice in answer_data:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        chosen_choice=choice
                    )

        return response
    