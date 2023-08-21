from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_student=True)


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)


class User(AbstractUser): # ToDo: doc string is missing, timestamp created_at and updated_at is missing
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    objects = UserManager()
    students = StudentManager()
    teachers = TeacherManager()

    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name="users",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="users",
    )

    def __str__(self):
        return self.username


class Classroom(models.Model): # ToDo: doc string is missing, timestamp updated_at is missing
    name = models.CharField(max_length=128, null=False, blank=False, default="Class 1")
    students = models.ManyToManyField(
        User,
        related_name="students_classroom",
        limit_choices_to={"is_student": True},
        through="ClassroomStudentEnrolled",
    )
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_teacher": True}
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):# ToDo: doc string is missing, timestamp updated_at is missing
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

    answer_choices = [
        ("MULTIPLE", "Multiple"),
        ("SHORT", "Short"),
        ("TRUEFALSE", "TrueFalse"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(
        null=True,
        blank=True,
    )
    time_limit = models.IntegerField(default=60)
    difficulty_level = models.CharField(
        max_length=50, choices=difficulty_choices, default="Easy"
    )
    category = models.CharField(
        max_length=128, choices=category_choices, default="Maths"
    )
    quiz_type = models.CharField(
        max_length=128, choices=answer_choices, default="Short"
    )
    total_score = models.IntegerField()
    question_numbers = models.IntegerField(default=1)
    required_score = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_quizzes",
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    # last_date = models.DateTimeField(default = datetime.datetime.today)
    students = models.ManyToManyField(
        User,
        through="QuizAssignment",
        related_name="assigned_quizzes",
        limit_choices_to={"is_student": True},
    )
    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_questions(self):
        self.quiz_question.all()


class Question(models.Model):# ToDo: doc string is missing, timestamp created_at and updated_at is missing
    answer_choices = [
        ("SHORT", "Short"),
        ("TRUEFALSE", "True/False"),
    ]
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quiz_question"
    )
    question_text = models.CharField(max_length=255)
    answer_options = models.CharField(
        max_length=255, choices=answer_choices, default="Short"
    )
    correct_answer = models.CharField(max_length=255)
    score = models.IntegerField()

    def __str__(self):
        return self.question_text

    def get_answer(self):
        return self.question_answer.all()

    def clean(self):
        if self.answer_options == "TRUEFALSE":
            if self.correct_answer == "True" or "TRUE" or "true":
                self.correct_answer = "TRUE"
            if self.correct_answer == "False" or "FALSE" or "false":
                self.correct_answer = "FALSE"


class Answer(models.Model):# ToDo: doc string is missing, timestamp updated_at is missing
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_answer"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Question :{self.question.question_text} Correct Answer: {self.is_correct}"
        )


class LeaderScores(models.Manager):# ToDo: doc string is missing
    def get_queryset(self):
        return super().get_queryset().order_by("-score")[:5]


class QuizScore(models.Model):# ToDo: doc string is missing, timestamp created_at and updated_at is missing
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    status_pass = models.BooleanField(default=False)
    objects = models.Manager()
    leaders = LeaderScores()

    def __str__(self):
        return f"{self.user_id} - {self.quiz_id} - {self.score}"


class ClassroomStudentEnrolled(models.Model):# ToDo: doc string is missing, timestamp updated_at is missing
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_student": True}
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.classroom} - {self.student}"


class QuizAssignment(models.Model):# ToDo: doc string is missing, timestamp created_at and updated_at is missing
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Quiz_Assignments"

    def __str__(self):
        return f"{self.student} - {self.quiz}"

# ToDO: use the Timestamp inheritance as did in past to remove the duplication