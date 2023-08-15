import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# import quizapp.base.routing as router
from base import routing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter(
        routing.websocket_urlpatterns
    )
})

print("Inside asgii")