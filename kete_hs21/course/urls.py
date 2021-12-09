from django.urls import path
from . import views

urlpatterns = [
    path("", views.courses, name="courses"),
    path("create", views.create, name="courses_create"),
    path("<int:course_id>/update", views.update, name="courses_update"),
    path("<int:course_id>/delete", views.delete, name="courses_delete"),
]
