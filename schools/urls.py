from .views import *
from django.urls import path

urlpatterns = [
  path("", home_view, name='home'),
  path("school/<str:id>",school_view, name="school"),
  path("students/", students_view, name="students"),
  path("teachers/", teachers_view, name="teachers"),
  path("nstaff/", nstaff_view, name="nstaff"),
]