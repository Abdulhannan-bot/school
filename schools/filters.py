import django_filters
# from django_filters import DateFilter

from .models import *

class SchoolFilter(django_filters.FilterSet):
  class Meta:
    model = School
    fields = ['name', 'phone']

class StudentFilter(django_filters.FilterSet):
  class Meta:
    model = Student
    fields = ['grade']

class TeacherFilter(django_filters.FilterSet):
  class Meta:
    model = Teacher
    fields = ['grade']

class AllStudentFilter(django_filters.FilterSet):
  class Meta:
    model = Student
    fields = ['name', 'school', 'grade']

class AllTeacherFilter(django_filters.FilterSet):
  class Meta:
    model = Teacher
    fields = ['name', 'school', 'grade']

class AllnStaffFilter(django_filters.FilterSet):
  class Meta:
    model = NonStaff
    fields = ['name', 'school', 'designation']