import uuid
import re
from os import path

import django.http
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from course.models import Course
from course.models import Lesson
from lesson.forms import LessonForm, RecordingForm, SlideshowForm

from django.contrib import messages


@login_required
def lessons(request, course_id):
    corresponding_course = get_object_or_404(Course, id=course_id)
    corresponding_lessons = Lesson.objects.filter(course=corresponding_course)
    context = {
        "lessons": corresponding_lessons,
        "course": corresponding_course,
        "is_teacher": request.user.groups.filter(name="teachers").exists()
    }
    return render(request=request, template_name="lesson/lessons.html", context=context)


@login_required()
def delete(request, course_id, lesson_id, needs_redirect=False):
    obj = get_object_or_404(Lesson, id=lesson_id)
    obj.delete()
    if needs_redirect:
        return redirect(lessons)
    return redirect(lessons, course_id)
    return django.http.HttpResponse()

def handle_uploaded_file(upload_file, upload_name=None):
    #yolo
    with open(path.join(settings.RECORDINGS_ROOT, upload_name), 'wb+') as destination:
        for chunk in upload_file.chunks():
            destination.write(chunk)

@login_required
def create(request, course_id):
    corresponding_course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        lesson_form = LessonForm(request.POST)
        recording_form = RecordingForm(request.POST)
        slideshow_form = SlideshowForm(request.POST)
        if lesson_form.is_valid():
            lesson_formdata = lesson_form.save(commit=False)
            lesson_formdata.created_by = request.user.profile
            lesson_formdata.course_id = corresponding_course.id
            lesson_formdata.save()
            lesson_form.save_m2m()
            messages.success(request, 'Lektion gespeichert.')
            if recording_form.is_valid() and recording_form.cleaned_data["recording_name"]:
                filename = str(uuid.uuid4()) + "_" + "".join([c for c in recording_form.cleaned_data["recording_name"] if re.match(r'\w', c)])
                handle_uploaded_file(request.FILES['recording_file'], upload_name=filename)
                recording_formdata = recording_form.save(commit=False)
                recording_formdata.lesson_id = lesson_formdata.id
                recording_formdata.save()
        else:
            messages.error(request, 'Fehler beim Speichern der Lektion.')
        return redirect(lessons, course_id)
    lesson_form = LessonForm()
    recording_form = RecordingForm()
    slideshow_form = SlideshowForm()
    return render(request=request, template_name="lesson/create.html", context={'lesson_form': lesson_form,
                                                                                "recording_form": recording_form,
                                                                                "slideshow_form": slideshow_form,
                                                                                'course': corresponding_course})