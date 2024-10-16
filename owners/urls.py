from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.owner_home, name='owner-home'),
]