from django.urls import path
from base import consumers

websocket_urlpatterns = [
    path('ws/sc/', consumers.QuizStatusSyncConsumer.as_asgi()),
    path('ws/ac/', consumers.QuizStatusAsyncConsumer.as_asgi()),
]