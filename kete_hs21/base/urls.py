from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('login', LoginView.as_view(), name="login_url"),
    #path('register/', views.registerView, name="register_url"),
    path('logout', LogoutView.as_view(next_page='dashboard'), name="logout"),
    path('welcome', views.welcome, name="home"),
    path('about', views.about, name="about"),
    path('', views.root, name="roots")
]
