from django.utils import timezone
from base.helpers import send_quiz_email
from base.models import QuizAssignment
from datetime import timedelta

def attempt_quizzes():
    """ This is function which is called after some specific time to send emails to those students whose
    quizzes are pending """
    quizzes = QuizAssignment.objects.filter(completed = False)
    for quiz in quizzes:
        scheduled_time = quiz.quiz.created + timedelta(days=1)
        now = timezone.now()
        if scheduled_time > now:
            send_quiz_email(quiz.student)
    print("Cron job was called")
