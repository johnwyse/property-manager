from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('resume', views.resume, name="resume")
]