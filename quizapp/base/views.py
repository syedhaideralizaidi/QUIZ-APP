from base64 import urlsafe_b64encode
from datetime import datetime

import cv2
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.http import HttpResponse , HttpResponseBadRequest , StreamingHttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.views import View
from django.views.generic import (
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from flask import Response , Flask

from .forms import AnswerForm
from .helpers import send_forgot_password_mail
from .models import User, Quiz, Question, QuizScore, QuizAssignment, Answer
from .tasks import test_func

def home(request):
    return render(request, "templates/base/home.html")


def login_admin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.filter(username=username).first()

        if User.objects.filter(username=username).exists():
            password = user.check_password(password)
        else:
            context = {
                "message": "You are not an admin, Login as Admin!",
                "title": "Login as Admin",
            }
            return render(request, "templates/base/invalid.html", context)

        print(user)
        if user is not None and password:
            print(user)
            login(request, user)
            print("Current User", request.user)
            return redirect("/dashboard_admin")
        else:
            context = {
                "message": "You are not an admin, Login as Admin!",
                "title": "Login as Admin",
            }
            return render(request, "templates/base/invalid.html", context)
    else:
        return render(request, "templates/base/login_admin.html")


def login_teacher(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username, password=password)
        except:
            context = {
                "message": "You are not a teacher, Signup First!",
                "title": "Go to home page for Sign Up.",
            }
            return render(request, "templates/base/invalid.html", context)
        if user is not None and user.is_teacher:
            print(user)
            login(request, user)
            print("Current User", request.user)
            return redirect("/dashboard_teacher")
        else:
            context = {
                "message": "You are not a teacher, Login as Student!",
                "title": "Reset Password Email sent to your Email",
            }
            return render(request, "templates/base/invalid.html", context)
    else:
        return render(request, "templates/base/login_teacher.html")


def login_student(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username, password=password)
        except:
            context = {
                "title": "No User, Sign Up first!",
                "message": "Please Sign Up before Login.",
            }
            return render(request, "templates/base/invalid.html", context)
        if user is not None and user.is_student:
            login(request, user)
            return redirect("/dashboard_student")
        else:
            context = {
                "title": "No User, Sign Up first!",
                "message": "Please Sign Up before Login.",
            }
            return render(request, "templates/base/invalid.html", context)
    else:
        return render(request, "templates/base/login_student.html")


def logout_user(request):
    logout(request)
    return redirect("/")


def forgot(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if not User.objects.filter(username=username).first():
            raise ValidationError("User not Found")
        user_obj = User.objects.filter(username=username).first()
        encoded_pk = urlsafe_b64encode(force_bytes(user_obj.pk))
        send_forgot_password_mail(user_obj, encoded_pk)
        context = {
            "message": "Check your email for new password.",
            "title": "Password Reset Link sent to your Email! ",
        }
        return render(request, "templates/base/invalid.html", context)
    else:
        return render(request, "templates/base/forgot_password.html")


def reset_password(request, pk, encode):
    if request.method == "POST":
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return HttpResponse(
                {"message": f"User with ID {pk} not found."},
            )
        print("User in Reset", user.username)
        new_password = request.POST.get("password")
        user.password = new_password
        user.save()
        return redirect("/")
    else:
        return render(request, "templates/base/reset_password.html")

def is_student(request):
    print("In student")
    request.user.is_student = True
    return redirect("/dashboard_student")

def is_teacher(request):
    request.user.is_teacher = True
    request.user.is_staff = True
    request.user.is_superuser = True

class SignupTeacher(CreateView):
    model = User
    template_name = "templates/base/signup_teacher.html"
    fields = ["username", "email", "password"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.is_teacher = True
        form.instance.is_staff = True
        form.instance.is_superuser = True
        return super().form_valid(form)


class SignupStudent(CreateView):
    model = User
    template_name = "templates/base/signup_student.html"
    fields = ["username", "email", "password"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.is_student = True
        return super().form_valid(form)


class DashboardTeacher(TemplateView):
    template_name = "templates/base/dashboard_teacher.html"


class DashboardStudent(TemplateView):
    test_func.delay()
    template_name = "templates/base/dashboard_student.html"


class DashboardAdmin(TemplateView):
    template_name = "templates/base/dashboard_admin.html"


class QuizCreation(CreateView):
    model = Quiz
    fields = "__all__"
    success_url = "/dashboard_teacher"


class QuizUpdateDetail(UpdateView):
    model = Quiz
    fields = [
        "title",
        "description",
        "time_limit",
        "difficulty_level",
        "category",
        "required_score",
    ]
    success_url = "/quiz_history_teacher"


class QuizDelete(DeleteView):
    model = Quiz
    success_url = "/quiz_history_teacher"


class QuestionsCreation(CreateView):
    model = Question
    fields = "__all__"
    success_url = "/dashboard_teacher"


class UpdateTeacherProfile(UpdateView):
    template_name = "templates/base/update_teacher.html"
    model = User
    fields = ["username", "email", "password"]
    success_url = "/"

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
        except Exception as e:
            return HttpResponseBadRequest("An error occurred")
        return super().form_valid(form)


class UpdateStudentProfile(UpdateView):
    template_name = "templates/base/update_student.html"
    model = User
    fields = ["username", "email", "password"]
    success_url = "/"

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
        except Exception as e:
            return HttpResponseBadRequest("An error occurred")
        return super().form_valid(form)


class LeaderScores(TemplateView):
    template_name = "templates/base/leader_scores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leader_scores"] = QuizScore.leaders.all()
        return context


class MyScores(TemplateView):
    template_name = "templates/base/student_scores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = QuizScore.objects.filter(user_id=self.request.user.pk)
        context["my_scores"] = student
        return context


class QuizHistoryViewStudent(TemplateView):
    template_name = "templates/base/quiz_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = QuizScore.objects.filter(user_id=self.request.user.pk)
        context["my_quizzes"] = student
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["my_quizzes"] = context["my_quizzes"].filter(
                quiz_id__category__icontains=search_input
            ) or context["my_quizzes"].filter(
                quiz_id__difficulty_level__icontains=search_input
            )
        context["search_input"] = search_input
        return context


class QuizHistoryViewTeacher(TemplateView):
    template_name = "templates/base/quiz_history_teacher.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = Quiz.objects.filter(teacher=self.request.user.pk)
        context["my_quizzes"] = teacher
        return context


class PendingQuizzes(TemplateView):
    template_name = "templates/base/pending_quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = QuizAssignment.objects.filter(
            student=self.request.user.pk, completed=False
        )
        context["my_quizzes"] = student
        return context


class StartQuiz(View):
    template_name = "templates/base/start_quiz.html"

    def get(self, request, pk=None):
        id = pk
        assigned_quiz = Quiz.objects.get(id=id)
        teacher = assigned_quiz.teacher
        date = datetime.now()
        questions = Question.objects.filter(quiz_id=assigned_quiz.pk)
        question_forms = []
        for question in questions:
            form = AnswerForm(question=question)
            question_forms.append((question, form))
        inital = {
            "teacher": teacher,
            "quiz": assigned_quiz,
            "date": date,
            "forms": question_forms,
        }
        return render(request, "templates/base/start_quiz.html", inital)

    def post(self, request, pk=None):
        quiz = Quiz.objects.get(id=pk)
        questions = Question.objects.filter(quiz_id=quiz.pk)
        answer = request.POST.getlist("answer_text")
        count = 0
        correct = False
        for question in questions:
            if question.correct_answer == answer[count]:
                correct = True
            elif question.correct_answer != answer[count]:
                correct = False
            ans = Answer.objects.create(
                question=question,
                answer_text=answer[count],
                is_correct=correct,
                user=self.request.user,
            )
            ans.save()
            count += 1

        # Checking Answers and Creating Scores
        correct_answers = Answer.objects.filter(
            user=self.request.user, question__quiz=quiz, is_correct=True
        ).distinct("question")

        total_score = 0
        for i in correct_answers:
            total_score += i.question.score

        required_score = quiz.required_score
        status_pass = False
        if total_score >= required_score:
            status_pass = True
        else:
            status_pass = False

        quizscore = QuizScore.objects.get_or_create(
            user_id=self.request.user,
            quiz_id=quiz,
            score=total_score,
            status_pass=status_pass,
        )

        # Checking end
        assignment = QuizAssignment.objects.get(quiz=quiz, student=self.request.user)
        assignment.completed = True
        assignment.save()
        id = quizscore[0].pk
        return redirect(f"/quiz_status/{id}/")


class QuizStatus(DetailView):
    model = QuizScore
    template_name = "templates/base/quiz_score.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz_score"] = self.object
        return context


class AdminTeacher(View):
    def get(self, request):
        teachers = User.objects.filter(is_teacher=True)
        context = {
            "teacher": teachers,
        }
        return render(request, "templates/base/admin_teacher.html", context)


class AdminStudent(View):
    def get(self, request):
        student = User.objects.filter(is_student=True)
        context = {
            "students": student,
        }
        return render(request, "templates/base/admin_students.html", context)


class CreateStudent(CreateView):
    template_name = "templates/base/student_form.html"
    model = User
    fields = ["username", "email", "password"]

    def post(self, request):
        super(CreateStudent, self).post(request)
        username = request.POST["username"]
        user = User.objects.get(username=username)
        user.is_student = True
        user.save()
        return redirect("dashboard-admin")


class UpdateStudent(UpdateView):
    model = User
    template_name = "templates/base/student_form.html"
    fields = ["username", "email", "password"]


class DeleteStudent(DeleteView):
    model = User
    template_name = "templates/base/delete_confirm.html"
    success_url = "/dashboard_teacher"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student"
        return context


class UpdateTeacher(UpdateView):
    model = User
    template_name = "templates/base/student_form.html"
    fields = ["username", "email", "password"]


class DeleteTeacher(DeleteView):
    model = User
    template_name = "templates/base/delete_confirm.html"
    success_url = "/dashboard_teacher"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Teacher"
        return context


class CreateTeacher(CreateView):
    template_name = "templates/base/teacher_form.html"
    model = User
    fields = ["username", "email", "password"]

    def post(self, request):
        super(CreateTeacher, self).post(request)
        username = request.POST["username"]
        user = User.objects.get(username=username)
        user.is_teacher = True
        user.save()
        return redirect("dashboard-admin")


class StudentAdminQuizzes(View):
    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
        quizzes = QuizScore.objects.filter(user_id=user)
        context = {"quizzes": quizzes}
        return render(request, "templates/base/student_admin_quizzes.html", context)


class TeacherAdminQuizzes(View):
    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
        quizzes = QuizScore.objects.filter(quiz_id__teacher=user)
        context = {"quizzes": quizzes}
        return render(request, "templates/base/teacher_admin_quizzes.html", context)


class Stats(TemplateView):
    template_name = "templates/base/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        labels = []

        new_data = []
        new_labels = []
        queryset = QuizScore.objects.all().order_by("-score")

        teacher_queryset = Quiz.objects.filter(teacher__is_teacher=True)

        for score in queryset:
            labels.append(score.quiz_id.title)
            data.append(score.score)

        for score in teacher_queryset:
            new_labels.append(score.teacher.username)
            new_data.append(score.time_limit)

        context["labels"] = labels
        context["data"] = data
        context["new_labels"] = new_labels
        context["new_data"] = new_data

        return context



def generate_frame():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        # if success :
        #     cv2.imshow('Frame' , frame)
        #     cv2.waitKey(0)
        #
        # camera.release()
        # cv2.destroyAllWindows()

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def video(request):
    return StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')


