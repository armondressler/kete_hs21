from django import forms
from django.forms import TextInput

from course.models import Lesson, Recording, Slideshow

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("name", "description", "tags")


class RecordingForm(forms.ModelForm):
    class Meta:
        model = Recording
        fields = ("recording_name", "recording_description", "recording_tags", "recording_file")

class SlideshowForm(forms.ModelForm):
    class Meta:
        model = Slideshow
        fields = ("slideshow_name", "slideshow_tags", "slideshow_file")

