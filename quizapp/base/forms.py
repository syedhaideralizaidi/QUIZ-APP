from django.forms import inlineformset_factory
from django import forms
from base.models import Quiz, Question, Answer


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
            # "students",
            "classroom",
            # "quiz_type",
        ]


class QuestionForm(forms.ModelForm):
    """ This form have all the fields of Question models which is needed for the quiz. It is used in QuizFormSet. """
    class Meta:
        model = Question
        fields = "__all__"


QuizFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    fields=("question_text", "answer_options", "correct_answer", "score"),
    extra=1,
    # fields = '__all__',
    can_delete=True,
    # max_num = 7,
    min_num=1,
)


class AnswerForm(forms.ModelForm):
    """ This is a form for students through which questions are displayed to the students during their quiz. """
    class Meta:
        model = Answer
        fields = ["answer_text"]
