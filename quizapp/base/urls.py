from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name = 'home'),
    path('teacher/signup', views.SignupTeacher.as_view(), name = 'teacher-signup'),
    path('student/signup', views.SignupStudent.as_view(), name = 'student-signup'),
    path('teacher/login', views.login_teacher, name = 'teacher-login'),
    path('student/login', views.login_student, name = 'student-login'),
    path('logout', views.logout_user, name = 'logout'),
    path('forgot', views.forgot, name = 'forgot-pw'),
    path('reset_pw/<str:pk>/<str:encode>/', views.reset_password, name = 'reset-pw'),
    path('dashboard_teacher', login_required(views.DashboardTeacher.as_view()), name = 'dashboard-teacher'),
    path('dashboard_student', login_required(views.DashboardStudent.as_view()), name = 'dashboard-student'),
    path('update_teacher/<str:pk>/', login_required(views.UpdateTeacherProfile.as_view()), name = 'update-teacher'),
    path('update_student/<str:pk>/', login_required(views.UpdateStudentProfile.as_view()), name = 'update-student'),
    path('quiz_create', login_required(views.QuizCreation.as_view()), name = 'quiz-create'),
    path('question_create', login_required(views.QuestionsCreation.as_view()), name = 'question-create'),
    path('leaders', login_required(views.LeaderScores.as_view()), name = 'leaders'),
    path('myscores', login_required(views.MyScores.as_view()), name = 'myscores'),
    path('quiz_history', login_required(views.QuizHistoryViewStudent.as_view()), name = 'quiz-history'),


]
