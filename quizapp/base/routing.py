from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/sc/<pk>", consumers.MySyncConsumer.as_asgi()),
    path("ws/ac/<pk>", consumers.MyAsyncConsumer.as_asgi()),
]
