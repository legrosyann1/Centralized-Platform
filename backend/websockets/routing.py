from django.urls import re_path
from websockets.consumers import ActionsConsumer

websocket_urlpatterns = [
    re_path(r'actions/', ActionsConsumer.as_asgi())
]