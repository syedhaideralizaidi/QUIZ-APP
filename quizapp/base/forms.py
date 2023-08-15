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
            # "students",
            "classroom",
            # "quiz_type",
        ]


class QuestionForm(forms.ModelForm):
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
    class Meta:
        model = Answer
        fields = ["answer_text"]

    # def __init__(self, *args, **kwargs):
    #     question = kwargs.pop("question", None)
    #     super().__init__(*args, **kwargs)
    #     if question:
    #         self.initial["question"] = question
    #
    #     answer_options = question.answer_options if question else None
    #     if answer_options == "TRUEFALSE":
    #         self.fields["answer_text"] = forms.ChoiceField(
    #             choices = [("True", "True"), ("False", "False")],
    #             widget = forms.RadioSelect,
    #             required = True,
    #         )
    #     # if question.answer_options == "TRUEFALSE":
    #     #     self.fields["answer_text"] = forms.BooleanField(
    #     #         # widget = forms.RadioSelect ,
    #     #         required = True,
    #     #     )
    #     elif question.answer_options == "Short":
    #         pass
    #     else:
    #         # add additional fields for other answer options
    #         pass

            # for i in range(question.num_choices):
            #     self.fields[f"choice_{i}"] = forms.CharField(required = True)

