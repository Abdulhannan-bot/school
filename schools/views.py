from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.models import Group, User

# Create your views here.
from .filters import *
from .models import *

def home_view(request):
  school = School.objects.all()
  student = Student.objects.all()
  # teacher = Teacher.objects.all()
  my_filter_school = SchoolFilter(request.GET, queryset = school)
  school_list = my_filter_school.qs

  student_count = 0
  teacher_count = 0
  nstaff_count = 0
  for i in school_list.values_list('name'):
    # s = School.objects.get(name = i[0]).id
    student_count = student_count + School.objects.get(name = i[0]).student_set.count()
    teacher_count = teacher_count + School.objects.get(name = i[0]).teacher_set.count()
    nstaff_count = nstaff_count + School.objects.get(name = i[0]).nonstaff_set.count()

  # print(School.child_set)
  paginator = Paginator(school_list, 5)
  page_number = request.GET.get('page',1)
  page = paginator.get_page(page_number)

  
  context = {
    "school_count": school_list.count(),
    "student_count": student_count,
    "teacher_count": teacher_count,
    "nstaff_count": nstaff_count,
    "my_filter_school": my_filter_school,
    "page_range": paginator.get_elided_page_range(number = page_number),
    "page": page,
  }
  return render(request, "dashboard.html", context = context)

def school_view(request, id):
  school = School.objects.get(id = id)
  student = school.student_set.all()
  teacher = school.teacher_set.all()
  nstaff = school.nonstaff_set.all()

  my_filter_student = StudentFilter(request.GET, queryset = student)
  student_list = my_filter_student.qs

  paginator_student = Paginator(student_list, 1)
  page_number_student = request.GET.get('page_student',1)
  page_student = paginator_student.get_page(page_number_student)

  my_filter_teacher = TeacherFilter(request.GET, queryset = teacher)
  teacher_list = my_filter_teacher.qs

  paginator_teacher = Paginator(teacher_list, 1)
  page_number_teacher = request.GET.get('page_teacher',1)
  page_teacher = paginator_teacher.get_page(page_number_teacher)

  print(student_list.count())
  print(teacher_list.count())

  context = {
    "school": school,
    "student_count": student_list.count(),
    "teacher_count": teacher_list.count(),
    "my_filter_student": my_filter_student,
    "my_filter_teacher": my_filter_teacher,
    "page_student_range": paginator_student.get_elided_page_range(number = page_number_student),
    "page_teacher_range": paginator_teacher.get_elided_page_range(number = page_number_teacher),
    "page_student": page_student,
    "page_teacher": page_teacher,
    "nstaff": nstaff,
  }

  return render(request, "school.html", context = context)

def students_view(request):
  student = Student.objects.all()
  my_filter = AllStudentFilter(request.GET, queryset = student)
  student_list = my_filter.qs

  paginator = Paginator(student_list, 10)
  page_number = request.GET.get('page',1)
  page = paginator.get_page(page_number)

  context = {
    "student_count": student_list.count(),
    "my_filter": my_filter,
    "paginator_range": paginator.get_elided_page_range(number = page_number),
    "page": page,
  }

  return render(request, "student.html", context = context)

def students_view(request):
  student = Student.objects.all()
  my_filter = AllStudentFilter(request.GET, queryset = student)
  student_list = my_filter.qs

  paginator = Paginator(student_list, 10)
  page_number = request.GET.get('page',1)
  page = paginator.get_page(page_number)

  context = {
    "student_count": student_list.count(),
    "my_filter": my_filter,
    "paginator_range": paginator.get_elided_page_range(number = page_number),
    "page": page,
  }

  return render(request, "student.html", context = context)

def teachers_view(request):
  teacher = Teacher.objects.all()
  my_filter = AllTeacherFilter(request.GET, queryset = teacher)
  teacher_list = my_filter.qs

  paginator = Paginator(teacher_list, 10)
  page_number = request.GET.get('page',1)
  page = paginator.get_page(page_number)

  context = {
    "teacher_count": teacher_list.count(),
    "my_filter": my_filter,
    "paginator_range": paginator.get_elided_page_range(number = page_number),
    "page": page,
  }

  return render(request, "teacher.html", context = context)

def nstaff_view(request):
  nstaff = NonStaff.objects.all()
  my_filter = AllnStaffFilter(request.GET, queryset = nstaff)
  nstaff_list = my_filter.qs

  paginator = Paginator(nstaff_list, 10)
  page_number = request.GET.get('page',1)
  page = paginator.get_page(page_number)

  context = {
    "nstaff_count": nstaff_list.count(),
    "my_filter": my_filter,
    "paginator_range": paginator.get_elided_page_range(number = page_number),
    "page": page,
  }

  return render(request, "nstaff.html", context = context)