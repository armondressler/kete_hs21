from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('settings', views.settings, name="settings"),
    path('login', views.CustomLoginView.as_view(), name="login"),
    # path('register/', views.registerView, name="register_url"),
    path('logout', LogoutView.as_view(next_page='dashboard'), name="logout")
]