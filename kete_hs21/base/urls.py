from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('welcome', views.welcome, name="welcome"),
    path('about', views.about, name="about"),
    path('prototype_student', views.prototype_student, name="prototype_student"),
    path('prototype_teacher', views.prototype_teacher, name="prototype_teacher"),
    path('', views.root, name="roots")
]
