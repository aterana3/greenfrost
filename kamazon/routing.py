from django.urls import path
from kamazon.consumers.qrcode import QRConsumer
from kamazon.consumers.chat import ChatBotConsumer


websocket_urlpatterns = [
    path("ws/qr/<str:token>/", QRConsumer.as_asgi()),
    path("ws/chat/", ChatBotConsumer.as_asgi()),
]