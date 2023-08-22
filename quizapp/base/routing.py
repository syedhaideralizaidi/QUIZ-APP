from django.urls import path
from base import consumers

websocket_urlpatterns = [
    path('ws/sc/<pk>', consumers.QuizStatusSyncConsumer.as_asgi()),
    path('ws/ac/<pk>/', consumers.QuizStatusAsyncConsumer.as_asgi()),
]