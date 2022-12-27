from django.forms import ModelForm
from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import *

class SchoolForm(ModelForm):
  class Meta:
    model = School
    fields = '__all__'
    exclude = ['user']

# class StudentForm(ModelForm):
#   class Meta:
#     model = Student
#     field = '__all__'
#     exclude = ['user']

# class TeacherForm(ModelForm):
#   class Meta:
#     model = Teacher
#     field = '__all__'
#     exclude = ['user']