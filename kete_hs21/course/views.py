from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm
from django.contrib import messages


# Create your views here.
def courses(request):
    context = {
        "courses": Course.objects.all()
    }
    return render(request=request, template_name="courses.html", context=context)


def create(request):
    if request.method == "POST":
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            formdata = course_form.save(commit=False)
            formdata.created_by = request.user.profile
            formdata.save()
            #course_form.save()
            messages.success(request, 'Your movie was successfully added!')
        else:
            messages.error(request, 'Error saving form')
        return redirect(courses)
    course_form = CourseForm()
    all_courses = Course.objects.all()
    return render(request=request, template_name="create.html", context={'course_form': course_form, 'courses': all_courses})

