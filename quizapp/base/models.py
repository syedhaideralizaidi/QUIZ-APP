from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, null = False, blank = False)
    email = models.EmailField(unique=True, max_length = 255)
    password = models.CharField(max_length=128)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name = "users",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name = "users",
    )

    def __str__(self):
        return self.username

class Quiz(models.Model):
    difficulty_choices = [
        ("EASY", "Easy"),
        ("MEDIUM", "Medium"),
        ("HARD", "Hard"),
    ]
    category_choices = [
        ("SCIENCE", "Science"),
        ("MATHS", "Maths"),
        ("ENGLISH", "English"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True, )
    time_limit = models.IntegerField(default = 60)
    difficulty_level = models.CharField(max_length = 50, choices = difficulty_choices, default = "Easy")
    category = models.CharField(max_length = 128, choices = category_choices, default = "Maths")
    total_score = models.IntegerField()
    question_numbers = models.IntegerField(default = 1)
    required_score = models.IntegerField()
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

    def get_questions(self):
        self.quiz_question.all()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name = 'quiz_question')
    question_text = models.TextField(max_length = 255)
    answer_options = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length = 255)
    score = models.IntegerField()

    def __str__(self):
        return self.question_text

    def get_answer(self):
        return self.question_answer.all()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name = 'question_answer')
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Question :{self.question.question_text} Correct Answer: {self.is_correct}"


class QuizScore(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(null = False, blank = False)
    timestamp = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.user_id} - {self.quiz_id} - {self.score}"