from django.urls import path
from .views import *

app_name='main'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:link>/', Room.as_view(), name='room'),
    path('close/<slug:link>/', closeRoom, name='closeRoom'),
    path('verify/<slug:link>/', verifyRoomEntry, name='verifyRoomEntry'),
    path('verified/<slug:link>/', verifiedRoomEntry, name='verifiedRoomEntry'),
    path('update/<slug:link>/', updateMessage, name='updateMessage'),
    
]
