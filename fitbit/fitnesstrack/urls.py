from django.urls import path
from . import views

app_name = 'fitbit'

urlpatterns = [
    path('home/', views.home, name='home'),
]