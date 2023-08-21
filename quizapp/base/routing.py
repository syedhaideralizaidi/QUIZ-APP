from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/sc/<pk>", consumers.MySyncConsumer.as_asgi()), # ToDo: MysyncConsumer, it's name should be self explaining like what this consumer does
    path("ws/ac/<pk>", consumers.MyAsyncConsumer.as_asgi()), # ToDo: MyAsyncConsumer, it's name should be self explaining like what this consumer does
]
