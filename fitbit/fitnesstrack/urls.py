from django.urls import path
from . import views

app_name = 'fitbit'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('send_csv/', views.send_csv, name='send_csv'),
]
