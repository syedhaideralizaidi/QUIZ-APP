from django.db import transaction , IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect , render
from django.urls import reverse
from .models import User, QuizAssignment, ClassroomStudentEnrolled
from .forms import QuizForm, QuizFormSet

from django.views.generic.edit import CreateView
from .models import Quiz

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
                req = self.request.POST
                question_formset = context["question_formset"]
                students = User.students.all()
                number_count = 0
                if question_formset.is_valid():
                    count_questions = req[ 'quiz_question-TOTAL_FORMS' ]
                    count_questions = int(count_questions)
                    print(number_count)
                    for question in range(0 , count_questions) :
                        value = f'quiz_question-{question}-score'
                        number_count += int(req[ value ])

                    if number_count != int(req['total_score']) or req['required_score'] > req['total_score']:
                        return self.form_invalid(form)
                    else :
                        pass
                    quiz = form.save(commit = False)
                    quiz.teacher = self.request.user
                    quiz.save()
                    self.object = form.save()
                    question_formset.instance = self.object
                    question_formset.save()
                else:
                    return self.form_invalid(form)
                classroom = quiz.classroom
                for student in students:
                    if ClassroomStudentEnrolled.objects.filter(classroom = classroom, student = student).exists():
                        QuizAssignment.objects.get_or_create(quiz=quiz, student=student, completed=False, classroom = classroom)

                return redirect(reverse("dashboard-teacher"))

        except IntegrityError:
            print("Not allowed")
            return HttpResponse("IntegrityError")


    def form_invalid(self, form):
        context = self.get_context_data()
        question_formset = context["question_formset"]
        # return self.render_to_response(
        #     self.get_context_data(form=form, question_formset=question_formset)
        # )
        return render(self.request, 'templates/base/invalid.html', context = {'title': 'Invalid Form Submission.', 'message': 'Check if your required score is less than total score or your questions score total is equal to total score of Quiz.'} )
    def get_success_url(self):
        return redirect("/dashboard_teacher")

