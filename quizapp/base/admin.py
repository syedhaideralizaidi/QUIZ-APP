from django.contrib import admin
from .models import Quiz , QuizScore , Question , Answer , User , QuizAssignment , Student


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass

@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(QuizAssignment)
class QuizAssignmentAdmin(admin.ModelAdmin):
    pass