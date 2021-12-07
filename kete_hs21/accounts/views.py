from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'welcome.html'

@login_required()
def settings(request):
    return render(request, "settings.html")
