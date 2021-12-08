from django.db import models
from taggit.managers import TaggableManager

from base.models import Profile


class Course(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True, max_length=2048, verbose_name="Beschreibung")
    tags = TaggableManager(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    date_modified = models.DateTimeField(auto_now_add=True, verbose_name="Angepasst am")
    created_by = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="course_created_by", verbose_name="erstellt von")
    responsible_teachers = models.ManyToManyField(Profile, through="CourseResponsibleTeachers", related_name="course_responsible_teacher", verbose_name="Verantwortliche Dozenten")
    subscribed_students = models.ManyToManyField(Profile, through="CourseSubscribedStudents", related_name="course_subscribed_students", verbose_name="Eingeschriebene Studenten")


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, max_length=2048)
    tags = TaggableManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)


class CourseResponsibleTeachers(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)


class CourseSubscribedStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)


class Recording(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, max_length=2048)
    tags = TaggableManager()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Slidesshow(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, max_length=2048)
    tags = TaggableManager()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

