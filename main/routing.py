from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/sc/', RoomSocket.as_asgi()),
    path('ws/ac/', AsyncRoomSocket.as_asgi()),

]