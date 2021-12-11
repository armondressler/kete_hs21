from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons, name="lessons"),
    path("create", views.create, name="lessons_create"),
    path("<int:lesson_id>/delete", views.delete, name="lessons_delete")
]