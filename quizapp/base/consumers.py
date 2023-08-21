import os

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from django.contrib.auth import get_user_model
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
import django
django.setup()
from base.models import QuizAssignment


class QuizStatusSyncConsumer(SyncConsumer):
    """ This is a consumer which basically displays the completed and pending quizzes count with channels in django
    synchronously """

    def websocket_connect(self, event):
        print("Web socket connected...", event)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Web socket message received...", event)
        print("Received Message is: ", event['text'])
        User = get_user_model()
        user = User.objects.all()
        assigned_quiz = QuizAssignment.objects.filter(student = user[4], completed = False)
        completed_quiz = QuizAssignment.objects.filter(student = user[4], completed = True)

        self.send({
            'type': 'websocket.send',
            'text': f'Quizzes left: {assigned_quiz.count()} ---------- Quizzes completed: {completed_quiz.count()}'
        })

    def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        raise StopConsumer()


class QuizStatusAsyncConsumer(AsyncConsumer):
    """ This is a consumer which basically displays the completed and pending quizzes count with channels in django
        asynchronously """

    async def websocket_connect(self, event):
        print("Web socket connected...", event)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("Web socket message received...", event)
        print("Received Message is: ", event['text'])
        # assigned_quiz = QuizAssignment.objects.filter(student = 3).count()
        # if self.scope['user'].is_authenticated:

        await self.send({
            'type': 'websocket.send',
            'text': f'You have {0} quizzes left'
        })


    async def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        raise StopConsumer()

