from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm
from django.contrib import messages


# Create your views here.
@login_required
def courses(request):
    context = {
        "courses": Course.objects.all(),
        "is_teacher": request.user.groups.filter(name="teachers").exists()
    }
    return render(request=request, template_name="courses.html", context=context)

@login_required()
def delete(request, course_id):
    obj = get_object_or_404(Course, id=course_id)
    obj.delete()
    return redirect(courses)

@login_required
def create(request):
    if request.method == "POST":
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            formdata = course_form.save(commit=False)
            formdata.created_by = request.user.profile
            formdata.save()
            messages.success(request, 'Your movie was successfully added!')
        else:
            messages.error(request, 'Error saving form')
        return redirect(courses)
    course_form = CourseForm()
    all_courses = Course.objects.all()
    return render(request=request, template_name="create.html", context={'course_form': course_form, 'courses': all_courses})


@login_required
def update(request, course_id):
    obj = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Modul erfolgreich angepasst.")
        context = {'course_form': form}
        return redirect(courses)
    else:
        context = {'course_form': form,
                   'course': obj,
                   'error': 'Fehler beim Anpassen des Moduls.'}
        return render(request, template_name="update.html", context=context)
