# Generated by Django 3.2.9 on 2021-12-10 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_alter_recording_recording_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='recording_audio_archived_name',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='recording',
            name='recording_audio_split_task_status',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='recording',
            name='recording_audio_to_text_task_status',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='recording',
            name='recording_text_archived_name',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='recording',
            name='recording_video_archived_name',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
