from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_type, name='user-type'),
    path('register/user', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]