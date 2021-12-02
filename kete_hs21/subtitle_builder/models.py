from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=256)
    create_date = models.DateTimeField('date created')

class Subtitle(models.Model):
    text = models.TextField()
    create_date = models.DateTimeField('date created')
    create_account = models.CharField(max_length=256)
    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING)
