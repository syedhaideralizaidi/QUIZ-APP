from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager

class TimeStampModel(models.Model):
    """This is a timestamp model which creates track of all other models"""
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    class Meta:
        abstract = True

class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_student=True)


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)


class User(AbstractUser):
    """This is a user model which can be teacher, student or an admin"""
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
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

class Classroom(TimeStampModel):
    """This is a model for classroom which is created by teacher and consists of different students"""
    name = models.CharField(max_length = 128, null = False, blank = False, default = "Class 1")
    students = models.ManyToManyField(User, related_name = 'students_classroom', limit_choices_to = {'is_student': True}, through = 'ClassroomStudentEnrolled')
    teacher = models.ForeignKey(User, on_delete = models.CASCADE, limit_choices_to = {'is_teacher': True})

    def __str__(self):
        return self.name
class Quiz(TimeStampModel):
    """This is a quiz model which have all the necessary fields required for the quiz"""
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
        max_length = 128, choices = answer_choices, default = "Short"
    )
    total_score = models.IntegerField()
    question_numbers = models.IntegerField(default=1)
    required_score = models.IntegerField()
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_quizzes",
    )
    classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
    students = models.ManyToManyField(User, through = 'QuizAssignment', related_name = 'assigned_quizzes', limit_choices_to = {'is_student': True})
    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_questions(self):
        self.quiz_question.all()


class Question(TimeStampModel):
    """This is a questions model which is used by Quiz to create different questions inside one Quiz"""
    answer_choices = [
        ("SHORT", "Short"),
        ("MULTIPLE", "Multiple"),
        ("TRUEFALSE", "TrueFalse"),
    ]
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quiz_question"
    )
    question_text = models.CharField(max_length=255)
    answer_options = models.CharField(max_length=255, choices = answer_choices, default = "Short")
    correct_answer = models.CharField(max_length=255)
    score = models.IntegerField()

    def __str__(self):
        return self.question_text

    def get_answer(self):
        return self.question_answer.all()


class Answer(TimeStampModel):
    """This is an answer model which is related to Question model and Student when answers a question it gets created"""
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_answer"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Question :{self.question.question_text} Correct Answer: {self.is_correct}"
        )


class LeaderScores(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("-score")[:5]


class QuizScore(TimeStampModel):
    """This model have all the scores and status of students for a specific quiz"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(null=False, blank=False)
    status_pass = models.BooleanField(default=False)
    objects = models.Manager()
    leaders = LeaderScores()

    def __str__(self):
        return f"{self.user_id} - {self.quiz_id} - {self.score}"

class ClassroomStudentEnrolled(TimeStampModel):
    """This is a model which keeps track that which student is enrolled in which classroom"""
    classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
    student = models.ForeignKey(User, on_delete = models.CASCADE, limit_choices_to = {'is_student': True})
    def __str__(self):
        return f"{self.classroom} - {self.student}"

class QuizAssignment(TimeStampModel):
    """This model gets triggered when a teacher assigns any quiz to student, and it makes a relationship between Quiz
    and Student. It also keeps the track whether the quiz is completed or not."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)

    class Meta:
        verbose_name = "Quiz_Assignments"

    def __str__(self):
        return f"{self.student} - {self.quiz}"

