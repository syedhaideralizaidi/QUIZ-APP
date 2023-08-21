from django.contrib import admin
from base.models import Quiz, QuizScore, Question, Answer, User, QuizAssignment, Classroom, ClassroomStudentEnrolled
from django import forms

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)
    search_fields = ('username',)
    list_filter = ('is_student', 'is_teacher',)
    ordering = ('created_at', )


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'total_score','required_score', 'teacher')
    search_fields = ('category',)
    list_filter = ('category', 'teacher',)
    ordering = ('required_score', )
    readonly_fields = ("created_at",)

    def get_form(self, request, obj=None, **kwargs):
        kwargs["widgets"] = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter Quiz Title e.g. Quiz 1"}
            ),
            "category": forms.TextInput(attrs={"placeholder": "Enter Category"}),
            "total_score" : forms.TextInput(attrs = {"placeholder" : "Must be less then 100"}) ,
            "required_score": forms.TextInput(attrs={"placeholder": "Must be less then total score"}),
        }
        kwargs["labels"] = {
            "title": "Quiz Title",
            "category": "Quiz Category",
        }
        return super().get_form(request, obj, **kwargs)


@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ('score','quiz_id', 'user_id', 'status_pass')
    list_filter = ('status_pass',)
    ordering = ('created_at',)
    readonly_fields = ("created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'answer_options', 'correct_answer', 'score')
    list_filter = ('score',)
    ordering = ('created_at',)
    readonly_fields = ("created_at",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'user',  'is_correct')
    list_filter = ('is_correct',)
    ordering = ('created_at',)
    readonly_fields = ("created_at",)


@admin.register(QuizAssignment)
class QuizAssignmentAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'student', 'completed', 'classroom')
    list_filter = ('completed',)
    ordering = ('created_at',)
    actions = ["mark_as_complete"]
    readonly_fields = ("created_at",)

    def mark_as_complete(self, request, queryset):
        queryset.update(completed = True)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    list_filter = ('teacher',)
    ordering = ('created_at',)
    readonly_fields = ("created_at",)


@admin.register(ClassroomStudentEnrolled)
class ClassroomStudentEnrolledAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'student')
    list_filter = ('classroom',)
    ordering = ('created_at',)
    readonly_fields = ("created_at",)

