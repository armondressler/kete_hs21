from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses, name="courses"),
    path("create", views.create, name="courses_create")
]
