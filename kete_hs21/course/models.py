from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator

from base.models import Profile


class Course(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True, max_length=2048, verbose_name="Beschreibung")
    tags = TaggableManager(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    date_modified = models.DateTimeField(auto_now_add=True, verbose_name="Angepasst am")
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="course_created_by", verbose_name="erstellt von")
    responsible_teachers = models.ManyToManyField(Profile, through="CourseResponsibleTeachers", related_name="course_responsible_teacher", verbose_name="Verantwortliche Dozenten")
    subscribed_students = models.ManyToManyField(Profile, through="CourseSubscribedStudents", related_name="course_subscribed_students", verbose_name="Eingeschriebene Studenten")


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, max_length=2048, verbose_name="Beschreibung")
    tags = TaggableManager(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)


class CourseResponsibleTeachers(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)


class CourseSubscribedStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Recording(models.Model):
    recording_name = models.CharField(max_length=256, blank=True)
    recording_description = models.TextField(null=True, max_length=2048, verbose_name="Beschreibung", blank=True)
    recording_tags = TaggableManager(blank=True)
    recording_file = models.FileField(verbose_name="Aufnahme", default=None, blank=True)
    recording_video_archived_name = models.CharField(max_length=256, blank=True)
    recording_audio_archived_name = models.CharField(max_length=512, blank=True)
    recording_text_archived_name = models.CharField(max_length=512, blank=True)
    recording_text_json_archived_name = models.CharField(max_length=512, blank=True)
    recording_audio_split_task_status = models.CharField(max_length=256, blank=True)
    recording_audio_to_text_task_status = models.CharField(max_length=256, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Slideshow(models.Model):
    slideshow_name = models.CharField(max_length=256, blank=True)
    slideshow_tags = TaggableManager(blank=True)
    slideshow_file = models.FileField(verbose_name="Foliensatz", default=None, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

