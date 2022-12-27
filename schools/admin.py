from django.contrib import admin

# Register your models here.

from .models import *

class SchoolAdmin(admin.ModelAdmin):
  list_display = ['name', 'phone', 'email']
  search_fields = ['name']

admin.site.register(School, SchoolAdmin)

class TeacherAdmin(admin.ModelAdmin):
  list_display = ['name', 'phone', 'email', 'school']
  search_fields = ['name', 'school']

admin.site.register(Teacher, TeacherAdmin)

class StudentAdmin(admin.ModelAdmin):
  list_display = ['name', 'phone', 'email', 'school']
  search_fields = ['name', 'school']

admin.site.register(Student, StudentAdmin)

class NonStaffAdmin(admin.ModelAdmin):
  list_display = ['name', 'phone', 'email', 'school']
  search_fields = ['name', 'school']

admin.site.register(NonStaff, NonStaffAdmin)


