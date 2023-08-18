import datetime
from django.utils import timezone
from .helpers import send_quiz_email
from .models import QuizAssignment
from datetime import timedelta


def attempt_quizzes():
    print("In cron job at time:", datetime.datetime.now())
    quizzes = QuizAssignment.objects.filter(completed=False)
    for quiz in quizzes:
        scheduled_time = quiz.quiz.created + timedelta(days=1)
        now = timezone.now()
        if scheduled_time > now:
            send_quiz_email(quiz.student)
    print("Cron job was called")
