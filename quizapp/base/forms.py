from django.forms import inlineformset_factory
from django import forms
from .models import Quiz , Question , Answer


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit', 'difficulty_level', 'category', 'required_score']
        # fields = '__all__'
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

QuizFormSet = inlineformset_factory(
    Quiz,
    Question,
    form = QuestionForm,
    fields=('question_text', 'correct_answer', 'score'),
    extra=2,
    #fields = '__all__',
    can_delete=False,
    # max_num = 7,
    min_num = 1,

)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']
