from django.shortcuts import render, redirect

def welcome(request):
    return render(request, "welcome/welcome.html")

def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def root(request):
    return redirect(dashboard)

def about(request):
    return redirect("https://github.com/armondressler/kete_hs21/blob/main/README.md")
