from django.urls import path
from kamazon.consumers.qrcode import QRConsumer


websocket_urlpatterns = [
    path("ws/qr/<str:token>/", QRConsumer.as_asgi()),
]