from django.forms import inlineformset_factory
from django import forms
from .models import Quiz, Question, Answer


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            "title",
            "description",
            "time_limit",
            "difficulty_level",
            "category",
            "required_score",
            "total_score",
            "classroom",
        ]


class QuestionForm(forms.ModelForm):# ToDO: docstring is missing
    class Meta:
        model = Question
        fields = "__all__"

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        if self.instance.answer_options == "TRUEFALSE":
            if self.instance.correct_answer == "TRUE" or "true" or "True":
                self.instance.correct_answer = "TRUE"
            elif self.instance.correct_answer == "FALSE" or "false" or "False":
                self.instance.correct_answer = "FALSE"
            else:
                pass
        else:
            pass
        return cleaned_data


QuizFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    fields=("question_text", "answer_options", "correct_answer", "score"),
    extra=1,
    can_delete=True,
    min_num=1,
    can_delete_extra=True,
)


class AnswerForm(forms.ModelForm):# ToDO: docstring is missing
    class Meta:
        model = Answer
        fields = ["answer_text"]

    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)
        super().__init__(*args, **kwargs)
        if question:
            self.instance.question = question
        if self.instance.question.answer_options == "TRUEFALSE":
            name = f"answer_text_{question}"
            self.fields["answer_text"] = forms.ChoiceField(
                choices=[("TRUE", "TRUE"), ("FALSE", "FALSE")],
                widget=forms.CheckboxSelectMultiple({"name": name}),
                label="True or False",
                required=True,
                error_messages={"required": "Please select an answer."},
            )
