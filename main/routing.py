from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    # path('ws/sc/<str:link>/', RoomSocket.as_asgi()),
    path('ws/ac/<str:link>/', AsyncRoomSocket.as_asgi()),
]