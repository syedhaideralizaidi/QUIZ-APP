from django.http import HttpResponse
from django.shortcuts import redirect , render
from django.views.generic.edit import CreateView
from django.urls import reverse
from .models import Quiz, User
from .forms import QuizFormSet, QuizForm


class QuizCreateView(CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = "templates/base/quiz_question_form.html"
    success_url = "/dashboard_teacher"

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        user = User.objects.get(pk = current_user.pk)
        if user.is_teacher:
            context = super().get_context_data(**kwargs)
            if self.request.POST:
                context["question_formset"] = QuizFormSet(self.request.POST)
            else:
                context["question_formset"] = QuizFormSet()
            return context

    def form_valid(self, form):
        context = self.get_context_data()
        quiz = form.save(commit=False)
        quiz.teacher = self.request.user
        quiz.total_score = 100
        quiz.save()
        question_formset = context["question_formset"]
        students = User.students.all()
        for student in students:
            QuizAssignment.objects.create(quiz=quiz, student=student, completed=False)
        if question_formset.is_valid():
            self.object = form.save()
            question_formset.instance = self.object
            question_formset.save()
            return redirect(reverse("dashboard-teacher"))
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        question_formset = context["question_formset"]
        return self.render_to_response(
            self.get_context_data(form=form, question_formset=question_formset)
        )

    def get_success_url(self):
        return redirect("/dashboard_teacher")

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         data['questions'] = QuestionFormSet(self.request.POST)
    #     else:
    #         data['questions'] = QuestionFormSet()
    #     return data
    #
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     questions = context['questions']
    #     quiz = form.save(commit=False)
    #     quiz.teacher = self.request.user
    #     quiz.save()
    #     if questions.is_valid():
    #         questions.instance = quiz
    #         questions.save()
    #     return super().form_valid(form)


from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Quiz, QuizAssignment

# class QuizCreateView(CreateView):
#     model = Quiz
#     template_name = 'quiz_create.html'
#     fields = ['title', 'description', 'time_limit', 'difficulty_level', 'category', 'total_score', 'question_numbers', 'required_score']
#
#     def form_valid(self, form):
#         quiz = form.save(commit=False)
#         quiz.teacher = self.request.user
#         quiz.save()
#         students = Student.objects.all()
#         for student in students:
#             QuizAssignment.objects.create(quiz=quiz, student=student)
#         return super().form_valid(form)
