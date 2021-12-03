from django.shortcuts import render, redirect

def home(request):
    return render(request, "base/base.html")

def welcome(request):
    return render(request, "welcome/welcome.html")

def root(request):
    return redirect(welcome)