from django.contrib import admin
from .models import (
    Quiz,
    QuizScore,
    Question,
    Answer,
    User,
    QuizAssignment,
    Classroom,
    ClassroomStudentEnrolled,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin): # ToDo: create the admin views
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin): # ToDo: create the admin views
    pass


@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin): # ToDo: create the admin views
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin): # ToDo: create the admin views
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin): # ToDo: create the admin views
    pass


@admin.register(QuizAssignment)
class QuizAssignmentAdmin(admin.ModelAdmin): # ToDo: create the admin views
    pass


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin): # ToDo: create the admin views
    pass


@admin.register(ClassroomStudentEnrolled)
class ClassroomStudentEnrolledAdmin(admin.ModelAdmin): # ToDo: create the admin views
    pass
