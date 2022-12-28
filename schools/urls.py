from .views import *
from django.urls import path

urlpatterns = [
  path("", home_view, name="home"),
  path("login/", login_page, name="login"),
  path("school/<str:id>",school_view, name="school"),
  path("students/", students_view, name="students"),
  path("teachers/", teachers_view, name="teachers"),
  path("nstaff/", nstaff_view, name="nstaff"),
  path("logout/", logout_trigger, name="logout"),
  path("update-school/<str:id>/", update_school, name="update-school" ),
  path("update-student/<str:id>/", update_student, name="update-student" ),
  path("update-teacher/<str:id>/", update_teacher, name="update-teacher" ),
  path("update-nstaff/<str:id>/", update_nstaff, name="update-nstaff" ),
]