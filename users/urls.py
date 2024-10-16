from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_home, name='welcome'),
    path('home/', views.user_home, name='home'),
]