# Generated by Django 3.2.9 on 2021-12-08 23:25

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('course', '0012_auto_20211208_2252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recording',
            old_name='tags',
            new_name='recording_tags',
        ),
        migrations.RemoveField(
            model_name='recording',
            name='description',
        ),
        migrations.RemoveField(
            model_name='recording',
            name='file',
        ),
        migrations.RemoveField(
            model_name='recording',
            name='name',
        ),
        migrations.RemoveField(
            model_name='slideshow',
            name='file',
        ),
        migrations.RemoveField(
            model_name='slideshow',
            name='name',
        ),
        migrations.RemoveField(
            model_name='slideshow',
            name='tags',
        ),
        migrations.AddField(
            model_name='recording',
            name='recording_description',
            field=models.TextField(blank=True, max_length=2048, null=True, verbose_name='Beschreibung'),
        ),
        migrations.AddField(
            model_name='recording',
            name='recording_file',
            field=models.FileField(blank=True, default=None, upload_to='', verbose_name='Aufnahme'),
        ),
        migrations.AddField(
            model_name='recording',
            name='recording_name',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='slideshow',
            name='slideshow_file',
            field=models.FileField(blank=True, default=None, upload_to='', verbose_name='Foliensatz'),
        ),
        migrations.AddField(
            model_name='slideshow',
            name='slideshow_name',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='slideshow',
            name='slideshow_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
