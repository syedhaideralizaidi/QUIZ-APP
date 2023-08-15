from django.utils import timezone

from .helpers import send_quiz_email
from .models import QuizAssignment
from datetime import time, timedelta
from django_cron import CronJobBase, Schedule

def attempt_quizzes():
    quizzes = QuizAssignment.objects.filter(completed = False)
    for quiz in quizzes:
        scheduled_time = quiz.quiz.created + timedelta(days=1)
        now = timezone.now()
        if scheduled_time > now:
            send_quiz_email(quiz.student)
    print("Cron job was called")

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'base.my_cron_job'
    ALLOW_PARALLEL_RUNS = True
    RUN_AT_TIMES = ['11:40']

    def do(self):
        print("Hello")
        attempt_quizzes()
        print("Yes")