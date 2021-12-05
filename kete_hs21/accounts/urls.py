from django.urls import path
from . import views

urlpatterns = [
    path('login', views.CustomLoginView.as_view(), name="login"),
# path('register/', views.registerView, name="register_url"),
#path('logout', LogoutView.as_view(next_page='dashboard'), name="logout")
]