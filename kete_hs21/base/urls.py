from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('welcome', views.welcome, name="welcome"),
    path('about', views.about, name="about"),
    path('', views.root, name="roots")
]
