from django import forms

from course.models import Lesson


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("name", "description", "tags")
