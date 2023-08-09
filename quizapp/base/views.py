from base64 import urlsafe_b64encode
from datetime import datetime , timedelta

from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.http import HttpResponse , HttpResponseBadRequest
from django.shortcuts import render , redirect
from django.urls import reverse , reverse_lazy
from django.utils.encoding import force_bytes
from django.views import View
from django.views.generic import CreateView , TemplateView , UpdateView , DeleteView , FormView

from .forms import QuestionForm
from .helpers import send_forgot_password_mail
from .models import User , Quiz , Question , QuizScore , QuizAssignment


def home(request):
    return render(request, 'templates/base/home.html')

def login_teacher(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # user = authenticate(request, username=username, password=password)
        user = User.objects.get(username = username, password= password)
        if user is not None and user.is_teacher:
            print(user)
            login(request, user)
            print("Current User", request.user)
            return redirect("/dashboard_teacher")
        else:
            context = {'message': 'You are not a teacher, Login as Student!', 'title': 'Reset Password Email sent to your Email'}
            return render(
                request,
                'templates/base/invalid.html',
                context
            )
    else:
        return render(
            request, 'templates/base/login_teacher.html'
        )


def login_student(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #user = authenticate(request, username=username, password=password, is_student = True)
        user = User.objects.get(username = username, password= password)

        if user is not None and user.is_student:
            login(request, user)
            return redirect("/dashboard_student")
        else:
            context = {'title': 'No User, Sign Up first!', 'message': 'Please Sign Up before Login.'}
            return render(
                request,
                'templates/base/invalid.html',
                context
            )
    else:
        return render(
            request, 'templates/base/login_student.html'
        )

def logout_user(request):
    logout(request)
    return redirect("/")

def forgot(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        if not User.objects.filter(username=username).first():
            raise ValidationError("User not Found")
        user_obj = User.objects.filter(username=username).first()
        encoded_pk = urlsafe_b64encode(force_bytes(user_obj.pk))
        send_forgot_password_mail(user_obj, encoded_pk)
        context = {'message': 'Check your email for new password.', 'title': 'Password Reset Link sent to your Email! '}
        return render(request, 'templates/base/invalid.html', context)
    else:
        return render(request, 'templates/base/forgot_password.html')


def reset_password(request, pk, encode):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return HttpResponse(
                {"message": f"User with ID {pk} not found."},
            )
        print("User in Reset", user.username)
        new_password = request.POST.get('password')
        user.password = new_password
        user.save()
        return redirect('/')
    else:
        return render(request, 'templates/base/reset_password.html')




class SignupTeacher(CreateView):
    model = User
    template_name = 'templates/base/signup_teacher.html'
    fields = ['username', 'email', 'password']
    success_url = '/'

    def form_valid(self, form):
        form.instance.is_teacher = True
        form.instance.is_staff = True
        form.instance.is_superuser = True
        # form.set_password(form.cleaned_data['password'])
        return super().form_valid(form)

class SignupStudent(CreateView):
    model = User
    template_name = 'templates/base/signup_student.html'
    fields = ['username', 'email', 'password']
    success_url = '/'

    def form_valid(self, form):
        form.instance.is_student = True
        return super().form_valid(form)

class DashboardTeacher(TemplateView):
    template_name = 'templates/base/dashboard_teacher.html'

class DashboardStudent(TemplateView):
    template_name = 'templates/base/dashboard_student.html'

class QuizCreation(CreateView):
    model = Quiz
    fields = '__all__'
    success_url = '/dashboard_teacher'

class QuizUpdateDetail(UpdateView):
    model = Quiz
    fields = ['title', 'description', 'time_limit', 'difficulty_level', 'category', 'required_score']
    success_url = '/quiz_history_teacher'

class QuizDelete(DeleteView):
    model = Quiz
    success_url = '/quiz_history_teacher'

class QuestionsCreation(CreateView):
    model = Question
    fields = '__all__'
    success_url = '/dashboard_teacher'

class UpdateTeacherProfile(UpdateView):
    template_name = 'templates/base/update_teacher.html'
    model = User
    fields = ['username', 'email', 'password']
    success_url = '/'

    def get_object(self, queryset=None):
        pk = self.kwargs["pk"]
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return render(
                self.request,
                "templates/base/invalid.html",
            )

    def form_valid(self, form):
        try:
            form.save()
            # user = form.instance
            # login(self.request, user)
        except Exception as e:
            return HttpResponseBadRequest("An error occurred")
        return super().form_valid(form)


class UpdateStudentProfile(UpdateView):
    template_name = 'templates/base/update_student.html'
    model = User
    fields = ['username', 'email', 'password']
    success_url = '/'

    def get_object(self, queryset=None):
        pk = self.kwargs["pk"]
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return render(
                self.request,
                "templates/base/invalid.html",
            )

    def form_valid(self, form):
        try:
            form.save()
            # user = form.instance
            # login(self.request, user)
        except Exception as e:
            return HttpResponseBadRequest("An error occurred")
        return super().form_valid(form)

class LeaderScores(TemplateView):
    template_name = 'templates/base/leader_scores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leader_scores"] = QuizScore.leaders.all()
        return context

class MyScores(TemplateView):
    template_name = 'templates/base/student_scores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = QuizScore.objects.filter(user_id = self.request.user.pk)
        context["my_scores"] = student
        return context

class QuizHistoryViewStudent(TemplateView):
    template_name = 'templates/base/quiz_history.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = QuizScore.objects.filter(user_id = self.request.user.pk)
        context["my_quizzes"] = student
        return context

class QuizHistoryViewTeacher(TemplateView):
    template_name = 'templates/base/quiz_history_teacher.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = Quiz.objects.filter(teacher = self.request.user.pk)
        context["my_quizzes"] = teacher
        return context

class PendingQuizzes(TemplateView):
    template_name = 'templates/base/pending_quiz.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = QuizAssignment.objects.filter(student = self.request.user.pk, completed = False)
        context["my_quizzes"] = student
        return context

class StartQuiz(View):
    template_name = 'templates/base/start_quiz.html'
    def get(self, request, pk = None):
        id = pk
        assigned_quiz = Quiz.objects.get(id = id)
        teacher = assigned_quiz.teacher
        date = datetime.now()
        questions = Question.objects.filter(quiz_id = assigned_quiz.pk)
        inital = {'teacher': teacher, 'quiz': assigned_quiz, 'date':date}
        return render(request, 'templates/base/start_quiz.html', inital)

    def post(self, request, pk = None):
        id = pk
        return redirect("dashboard-student")

