from django.urls import path
from .views import *

app_name='cadmin'

urlpatterns = [
    path('', CadminDashboard.as_view(), name='cadmin_dashboard'),
    path('verify-admin/', verifyCadmin, name='verifyAdmin'),
]
