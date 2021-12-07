# Generated by Django 3.2.9 on 2021-12-07 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20211207_0208'),
        ('course', '0003_auto_20211207_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='responsible_teachers',
            field=models.ManyToManyField(related_name='course_responsible_teacher', through='course.CourseResponsibleTeachers', to='base.Profile'),
        ),
        migrations.AlterField(
            model_name='course',
            name='subscribed_students',
            field=models.ManyToManyField(related_name='course_subscribed_students', through='course.CourseSubscribedStudents', to='base.Profile'),
        ),
    ]
