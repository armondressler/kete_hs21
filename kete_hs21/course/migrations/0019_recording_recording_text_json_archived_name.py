# Generated by Django 3.2.9 on 2021-12-15 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0018_alter_recording_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='recording_text_json_archived_name',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
