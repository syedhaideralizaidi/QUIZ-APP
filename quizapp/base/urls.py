from django.urls import path
from . import views, pdf_view, classroom_views
from . import formset_view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.home, name="home"),
    path("teacher/signup", views.SignupTeacher.as_view(), name="teacher-signup"),
    path("student/signup", views.SignupStudent.as_view(), name="student-signup"),
    path("teacher/login", views.login_teacher, name="teacher-login"),
    path("student/login", views.login_student, name="student-login"),
    path("login/admin", views.login_admin, name="admin"),
    path("logout", views.logout_user, name="logout"),
    path("forgot", views.forgot, name="forgot-pw"),
    path("reset_pw/<str:pk>/<str:encode>/", views.reset_password, name="reset-pw"),
    path(
        "dashboard_teacher",
        login_required(views.DashboardTeacher.as_view()),
        name="dashboard-teacher",
    ),
    path(
        "dashboard_student",
        login_required(views.DashboardStudent.as_view()),
        name="dashboard-student",
    ),
    path(
        "dashboard_admin",
        login_required(views.DashboardAdmin.as_view()),
        name = "dashboard-admin",
    ),
    path(
        "update_teacher/<str:pk>/",
        login_required(views.UpdateTeacherProfile.as_view()),
        name="update-teacher",
    ),
    path(
        "update_student/<str:pk>/",
        login_required(views.UpdateStudentProfile.as_view()),
        name="update-student",
    ),
    # path('quiz_create', login_required(views.QuizCreation.as_view()), name = 'quiz-create'),
    # path('question_create', login_required(views.QuestionsCreation.as_view()), name = 'question-create'),
    path("leaders", login_required(views.LeaderScores.as_view()), name="leaders"),
    path("myscores", login_required(views.MyScores.as_view()), name="myscores"),
    path(
        "quiz_history",
        login_required(views.QuizHistoryViewStudent.as_view()),
        name="quiz-history",
    ),
    path(
        "quiz_history_teacher",
        login_required(views.QuizHistoryViewTeacher.as_view()),
        name="quiz-history-teacher",
    ),
    path(
        "quiz_update/<int:pk>/",
        login_required(views.QuizUpdateDetail.as_view()),
        name="quiz-update",
    ),
    path(
        "quiz_delete/<int:pk>/",
        login_required(views.QuizDelete.as_view()),
        name="quiz-delete",
    ),
    path(
        "pending-quiz",
        login_required(views.PendingQuizzes.as_view()),
        name="pending-quiz",
    ),
    path(
        "quiz_create",
        login_required(formset_view.QuizCreateView.as_view()),
        name="quiz-create",
    ),
    path(
        "quiz_start/<int:pk>",
        login_required(views.StartQuiz.as_view()),
        name="quiz-start",
    ),
    path(
        "quiz_status/<int:pk>",
        login_required(views.QuizStatus.as_view()),
        name = "quiz-status",
    ),
    path(
        "teachers",
        login_required(views.AdminTeacher.as_view()),
        name = "teachers",
    ),
    path(
        "students",
        login_required(views.AdminStudent.as_view()),
        name = "students",
    ),
    path(
        "student_create",
        login_required(views.CreateStudent.as_view()),
        name = "student-create",
    ),
    path(
        "student_update/<int:pk>/",
        login_required(views.UpdateStudent.as_view()),
        name = "student-update",
    ),
    path(
        "student_delete/<int:pk>/",
        login_required(views.DeleteStudent.as_view()),
        name = "student-delete",
    ),
    path(
        "teacher_create",
        login_required(views.CreateTeacher.as_view()),
        name = "teacher-create",
    ),
    path(
        "teacher_update/<int:pk>/",
        login_required(views.UpdateTeacher.as_view()),
        name = "teacher-update",
    ),
    path(
        "teacher_delete/<int:pk>/",
        login_required(views.DeleteTeacher.as_view()),
        name = "teacher-delete",
    ),
    path(
        "quizzes_student/<int:pk>/",
        login_required(views.StudentAdminQuizzes.as_view()),
        name = "student-admin-quizzes",
    ),
    path(
        "quizzes_teacher/<int:pk>/",
        login_required(views.TeacherAdminQuizzes.as_view()),
        name = "teacher-admin-quizzes",
    ),
    path(
        "stats/",
        login_required(views.Stats.as_view()),
        name = "stats",
    ),
    path(
        "pdf/<int:pk>/",
        login_required(pdf_view.pdf),
        name = "pdf",
    ),
    path(
        "classroom_create",
        login_required(classroom_views.ClassroomCreate.as_view()),
        name = "create-classroom",
    ),
    path(
        "classroom_update/<str:pk>",
        login_required(classroom_views.ClassroomUpdate.as_view()),
        name = "update-classroom",
    ),
    path(
        "classroom_delete/<str:pk>",
        login_required(classroom_views.ClassroomDelete.as_view()),
        name = "delete-classroom",
    ),
    path(
        "classrooms",
        login_required(classroom_views.ClassroomTemplate.as_view()),
        name = "classrooms",
    ),
    path(
        "classrooms_student",
        login_required(classroom_views.ClassroomStudentTemplate.as_view()),
        name = "classrooms-student",
    ),

]
