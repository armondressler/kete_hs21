# Generated by Django 3.2.9 on 2021-12-06 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_student_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='location',
        ),
        migrations.AddField(
            model_name='customuser',
            name='deleteme',
            field=models.TextField(max_length=20, null=True),
        ),
    ]
