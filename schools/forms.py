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

class UpdateStudentForm(ModelForm):
  class Meta:
    model = Student
    fields = '__all__'
    exclude = ['user', 'school', 'grade']

class UpdateTeacherForm(ModelForm):
  class Meta:
    model = Teacher
    fields = '__all__'
    exclude = ['user', 'school', 'grade']

class UpdateNonStaffForm(ModelForm):
  class Meta:
    model = NonStaff
    fields = '__all__'
    exclude = ['user', 'school', 'grade']

class UpdateSchoolForm(ModelForm):
  class Meta:
    model = School
    fields = '__all__'
    exclude = ['user']

class CreateStudentForm(ModelForm):
  class Meta:
    fields = '__all__'

class CreateTeacherForm(ModelForm):
  class Meta:
    fields = '__all__'

class CreateNonStaff(ModelForm):
  class Meta:
    fields = '__all__'


