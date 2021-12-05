from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request, "welcome/welcome.html")

@login_required()
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def root(request):
    return redirect(dashboard)

def about(request):
    return redirect("https://github.com/armondressler/kete_hs21/blob/main/README.md")
