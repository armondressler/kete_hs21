# Generated by Django 3.2.9 on 2021-12-10 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_auto_20211210_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='recording_description',
            field=models.TextField(blank=True, max_length=2048, null=True, verbose_name='Beschreibung'),
        ),
    ]
