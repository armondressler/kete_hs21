from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from course.models import Course
from course.models import Lesson
from lesson.forms import LessonForm


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


@login_required
def create(request, course_id):
    corresponding_course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        lesson_form = LessonForm(request.POST)
        if lesson_form.is_valid():
            formdata = lesson_form.save(commit=False)
            formdata.created_by = request.user.profile
            formdata.save()
            #messages.success(request, 'Your movie was successfully added!')
        else:
            pass
            #messages.error(request, 'Error saving form')
        return redirect(lessons)
    lesson_form = LessonForm()
    return render(request=request, template_name="lesson/create.html", context={'lesson_form': lesson_form, 'course': corresponding_course})