from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from course.views import courses

def welcome(request):
    return render(request, "welcome/welcome.html")

@login_required()
def dashboard(request):
    return redirect(courses)

@login_required()
def root(request):
    return redirect(dashboard)

def about(request):
    return redirect("https://github.com/armondressler/kete_hs21/blob/main/README.md")

def prototype_student(request):
    return redirect("/prototype/student")

def prototype_teacher(request):
    return redirect("/prototype/teacher")
