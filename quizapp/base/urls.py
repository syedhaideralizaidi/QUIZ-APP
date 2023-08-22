from django.urls import path
from base import views, pdf_view, classroom_views
from base import formset_view
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
    path("reset/<str:pk>/<str:encode>/", views.reset_password, name="reset-pw"),
    path(
        "teacher",
        login_required(views.DashboardTeacher.as_view()),
        name="dashboard-teacher",
    ),
    path(
        "student",
        login_required(views.DashboardStudent.as_view()),
        name="dashboard-student",
    ),
    path(
        "admin",
        login_required(views.DashboardAdmin.as_view()),
        name = "dashboard-admin",
    ),
    path(
        "teacher/<str:pk>/",
        login_required(views.UpdateTeacherProfile.as_view()),
        name="update-teacher",
    ),
    path(
        "student/<str:pk>/",
        login_required(views.UpdateStudentProfile.as_view()),
        name="update-student",
    ),
    path("leaders", login_required(views.LeaderScores.as_view()), name="leaders"),
    path("scores", login_required(views.MyScores.as_view()), name="myscores"),
    path(
        "student/history",
        login_required(views.QuizHistoryViewStudent.as_view()),
        name="quiz-history",
    ),
    path(
        "quiz/history",
        login_required(views.QuizHistoryViewTeacher.as_view()),
        name="quiz-history-teacher",
    ),
    path(
        "quiz/<int:pk>/update",
        login_required(views.QuizUpdateDetail.as_view()),
        name="quiz-update",
    ),
    path(
        "quiz/<int:pk>/delete",
        login_required(views.QuizDelete.as_view()),
        name="quiz-delete",
    ),
    path(
        "pending/quizzes",
        login_required(views.PendingQuizzes.as_view()),
        name="pending-quiz",
    ),
    path(
        "create/quiz",
        login_required(formset_view.QuizCreateView.as_view()),
        name="quiz-create",
    ),
    path(
        "quiz/<int:pk>",
        login_required(views.StartQuiz.as_view()),
        name="quiz-start",
    ),
    path(
        "status/<int:pk>/",
        login_required(views.QuizStatus.as_view()),
        name = "quiz_status",
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
        "student/create",
        login_required(views.CreateStudent.as_view()),
        name = "student-create",
    ),
    path(
        "student/update/<int:pk>/",
        login_required(views.UpdateStudent.as_view()),
        name = "student-update",
    ),
    path(
        "student/delete/<int:pk>/",
        login_required(views.DeleteStudent.as_view()),
        name = "student-delete",
    ),
    path(
        "teacher/create",
        login_required(views.CreateTeacher.as_view()),
        name = "teacher-create",
    ),
    path(
        "teacher/update/<int:pk>/",
        login_required(views.UpdateTeacher.as_view()),
        name = "teacher-update",
    ),
    path(
        "teacher/delete/<int:pk>/",
        login_required(views.DeleteTeacher.as_view()),
        name = "teacher-delete",
    ),
    path(
        "quizzes/student/<int:pk>/",
        login_required(views.StudentAdminQuizzes.as_view()),
        name = "student-admin-quizzes",
    ),
    path(
        "quizzes/teacher/<int:pk>/",
        login_required(views.TeacherAdminQuizzes.as_view()),
        name = "teacher-admin-quizzes",
    ),
    path(
        "statistics/",
        login_required(views.Stats.as_view()),
        name = "stats",
    ),
    path(
        "pdf/<int:pk>/",
        login_required(pdf_view.pdf_report_generator),
        name = "pdf",
    ),
    path(
        "classroom/create",
        login_required(classroom_views.ClassroomCreate.as_view()),
        name = "create-classroom",
    ),
    path(
        "classroom/<str:pk>/update",
        login_required(classroom_views.ClassroomUpdate.as_view()),
        name = "update-classroom",
    ),
    path(
        "classroom/<str:pk>/delete",
        login_required(classroom_views.ClassroomDelete.as_view()),
        name = "delete-classroom",
    ),
    path(
        "classrooms",
        login_required(classroom_views.ClassroomTemplate.as_view()),
        name = "classrooms",
    ),
    path(
        "classrooms/student",
        login_required(classroom_views.ClassroomStudentTemplate.as_view()),
        name = "classrooms-student",
    ),

]
