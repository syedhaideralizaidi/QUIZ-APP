from django.db import transaction , IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from base.models import User, QuizAssignment, ClassroomStudentEnrolled
from base.forms import QuizForm, QuizFormSet

from django.views.generic.edit import CreateView
from .models import Quiz

class QuizCreateView(CreateView):
    """ This class creates Quiz for students along with the Questions using a formset. """
    model = Quiz
    form_class = QuizForm
    template_name = "templates/base/teachers/quiz/quiz_question_form.html"
    success_url = "/teacher"

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        user = User.objects.get(pk = current_user.pk)
        if user.is_teacher:
            context = super().get_context_data(**kwargs)
            if self.request.POST:
                print(self.request.POST)
                context["question_formset"] = QuizFormSet(self.request.POST)
            else:
                context["question_formset"] = QuizFormSet()
            return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        try:
            with transaction.atomic():
                quiz = form.save(commit=False)
                quiz.teacher = self.request.user
                quiz.save()
                question_formset = context["question_formset"]
                students = User.students.all()
                if question_formset.is_valid():
                    self.object = form.save()
                    question_formset.instance = self.object
                    question_formset.save()
                else:
                    return HttpResponse("Invalid form Submission, Also fill the questions with the Quiz!. Fill it again")
                classroom = quiz.classroom
                for student in students:
                    if ClassroomStudentEnrolled.objects.filter(classroom = classroom, student = student).exists():
                        QuizAssignment.objects.get_or_create(quiz=quiz, student=student, completed=False, classroom = classroom)

                    return redirect(reverse("dashboard-teacher"))
                else:
                    return self.form_invalid(form)
        except IntegrityError:
            print("Not allowed")
            return HttpResponse("IntegrityError")


    def form_invalid(self, form):
        context = self.get_context_data()
        question_formset = context["question_formset"]
        return self.render_to_response(
            self.get_context_data(form=form, question_formset=question_formset)
        )

    def get_success_url(self):
        return redirect("/teacher")

