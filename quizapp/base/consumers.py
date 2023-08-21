import os
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
import django

django.setup()
from .models import QuizAssignment


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.user = self.scope['url_route']['kwargs']['pk']
        print("Web socket connected...", event)
        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        print("Web socket message received...", event)
        print("Received Message is: ", event["text"])
        User = get_user_model()
        user = User.objects.filter(pk = self.user).first()
        assigned_quiz = QuizAssignment.objects.filter(student=user, completed=False)
        completed_quiz = QuizAssignment.objects.filter(student=user, completed=True)

        self.send(
            {
                "type": "websocket.send",
                "text": f"""Quizzes left: {assigned_quiz.count()} 
                (Quizzes completed: {completed_quiz.count()})""",
            }
        )

    def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Web socket connected...", event)
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print("Web socket message received...", event)
        print("Received Message is: ", event["text"])

        await self.send(
            {"type": "websocket.send", "text": f"You have {0} quizzes left"}
        )

    async def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        raise StopConsumer()


class NewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('users', self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard('users', self.channel_name)

    async def send_jokes(self, event):
        text_message = event['text']
        await self.send(text_message)