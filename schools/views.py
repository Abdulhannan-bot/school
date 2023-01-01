from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages

# Create your views here.
from .filters import *
from .models import *
from .decorators import *
from .forms import *

@unauthenticated_user
def login_page(request):
  if(request.method == 'POST'):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      if(request.user.groups.all()[0].name == 'school'):
        return redirect('school',id = request.user.school.id)
      elif(request.user.groups.all()[0].name == 'teacher'):
        return redirect('school',id = request.user.teacher.school.id)
      elif(request.user.groups.all()[0].name == 'student'):
        return redirect('school',id = request.user.student.school.id)
      elif(request.user.groups.all()[0].name == 'non-staff'):
        return redirect('school',id = request.user.nonstaff.school.id)
      elif(request.user.groups.all()[0].name == 'admin'):
        return redirect('home')
      else:
        print('passes through all')
        return redirect('home')
      return redirect('home')
  return render(request, 'login.html')

@login_required(login_url = 'login')
@admin_only
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

    
  
  # if(request.user.groups.name is None):
  #   admin_check = True
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

@login_required(login_url = 'login')
def school_view(request, id):
  school = School.objects.get(id = id)
  student = school.student_set.all()
  teacher = school.teacher_set.all()
  nstaff = school.nonstaff_set.all()


  id_num = ""

  my_filter_student = StudentFilter(request.GET, queryset = student)
  student_list = my_filter_student.qs

  paginator_student = Paginator(student_list, 10)
  page_number_student = request.GET.get('page_student',1)
  page_student = paginator_student.get_page(page_number_student)

  my_filter_teacher = TeacherFilter(request.GET, queryset = teacher)
  teacher_list = my_filter_teacher.qs

  paginator_teacher = Paginator(teacher_list, 10)
  page_number_teacher = request.GET.get('page_teacher',1)
  page_teacher = paginator_teacher.get_page(page_number_teacher)
  log = ""
  admin_check = False
  school_check = False
  if(request.user.groups.all()[0].name == 'admin'):
    admin_check = True
  elif(request.user.groups.all()[0].name == 'school'):
    log = request.user.groups.all()[0].name
    id_num = request.user.school.id
    school_check = True
  elif(request.user.groups.all()[0].name == 'student'):
    log = request.user.groups.all()[0].name
    id_num = request.user.student.id
  elif(request.user.groups.all()[0].name == 'teacher'):
    log = request.user.groups.all()[0].name
    id_num = request.user.teacher.id
  elif(request.user.groups.all()[0].name == 'non-staff'):
    log = request.user.groups.all()[0].name
    id_num = request.user.nonstaff.id
  
  print(request.user.groups.all()[0].name)
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
    "admin_check": admin_check,
    "school_check": school_check,
    "id": id_num, 
    "log": log,
  }

  return render(request, "school.html", context = context)

@login_required(login_url = 'login')
@admin_only
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


@login_required(login_url = 'login')
@admin_only
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

@login_required(login_url = 'login')
@admin_only
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

def logout_trigger(request):
  logout(request)
  return redirect('login')

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['student'])
def update_student(request, id):
  student = Student.objects.get(id = id)
  school = request.user.student.school
  form = UpdateStudentForm(instance = student)
  if request.method == "POST":
    form = UpdateStudentForm(request.POST, instance = student)
    if form.is_valid():
      form.save()
      return redirect('/')
  context = {
    "form": form,
    "log": request.user.groups.all()[0].name,
    "id": student.id,
    "school": school,
  }
  return render(request, "update.html", context = context) 

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['teacher'])
def update_teacher(request, id):
  teacher = Teacher.objects.get(id = id)
  school = request.user.teacher.school
  form = UpdateTeacherForm(instance = teacher)
  if request.method == "POST":
    form = UpdateTeacherForm(request.POST, instance = teacher)
    if form.is_valid():
      form.save()
      return redirect('/')
  context = {
    "form": form,
    "log": request.user.groups.all()[0].name,
    "id": teacher.id,
    "school": school,
  }
  return render(request, "update.html", context = context) 

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['non-staff'])
def update_nstaff(request, id):
  nstaff = NonStaff.objects.get(id = id)
  school = request.user.nonstaff.school
  form = UpdateNonStaffForm(instance = nstaff)
  if request.method == "POST":
    form = UpdateNonStaffForm(request.POST, instance = nstaff)
    if form.is_valid():
      form.save()
      return redirect('/')
  context = {
    "form": form,
    "log": request.user.groups.all()[0].name,
    "id": nstaff.id,
    "school": school,
  }
  return render(request, "update.html", context = context) 

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['school'])
def update_school(request, id):
  school = School.objects.get(id = id)
  form = UpdateSchoolForm(instance = school)
  if request.method == "POST":
    form = UpdateSchoolForm(request.POST, request.FILES, instance = school)
    if form.is_valid():
      form.save()
      return redirect('/')
  print(f'name - {request.user.groups.all()[0].name}')
  context = {
    "form": form,
    "log": request.user.groups.all()[0].name,
    "school": school,
  }
  return render(request, "update.html", context = context) 

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['school'])
def delete_student(request, id):
  user = Student.objects.get(id = id).user
  User.objects.get(username = user).delete()
  return redirect('/')

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['school'])
def delete_teacher(request, id):
  user = Teacher.objects.get(id = id).user
  User.objects.get(username = user).delete()
  return redirect('/')

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['school'])
def delete_nstaff(request, id):
  user = NonStaff.objects.get(id = id).user
  User.objects.get(username = user).delete()
  return redirect('/')


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['school'])
def add_student(request,id):

  StudentFormset = inlineformset_factory(School, Student, fields=('name','email','phone','grade'), extra=5)
  school = School.objects.get(id = id)
  formset = StudentFormset(queryset = Student.objects.none(), instance=school) 
  # form = OrderForm(initial={'customer':customer})
  if request.method == 'POST':
    formset = StudentFormset(request.POST, instance=school)
    # form = OrderForm(request.POST)
    if formset.is_valid():
      formset.save()
      return redirect('/')
  context = {
    "school": school,
    "formset": formset,
  }
  return render(request, "add-student.html", context = context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['school'])
def add_teacher(request,id):
  TeacherFormset = inlineformset_factory(School, Teacher, fields=('name','email','phone','grade'), extra=5)
  school = School.objects.get(id = id)
  formset = TeacherFormset(queryset = Teacher.objects.none(), instance=school) 
  # form = OrderForm(initial={'customer':customer})
  if request.method == 'POST':
    formset = TeacherFormset(request.POST, instance=school)
    # form = OrderForm(request.POST)
    if formset.is_valid():
      formset.save()
      return redirect('/')
  context = {
    "school": school,
    "formset": formset,
  }
  return render(request, "add-student.html", context = context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['school'])
def add_nstaff(request,id):
  NstaffFormset = inlineformset_factory(School, NonStaff, fields=('name','email','phone','designation'), extra=5)
  school = School.objects.get(id = id)
  formset = NstaffFormset(queryset = NonStaff.objects.none(), instance=school) 
  # form = OrderForm(initial={'customer':customer})
  if request.method == 'POST':
    formset = NstaffFormset(request.POST, instance=school)
    # form = OrderForm(request.POST)
    if formset.is_valid():
      formset.save()
      return redirect('/')
  context = {
    "school": school,
    "formset": formset,
  }
  return render(request, "add-student.html", context = context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['teacher','non-staff'])
def remarks_view(request):
  school = ""
  if(request.user.groups.all()[0].name == "teacher"):
    id = request.user.teacher.school.id
    school = School.objects.get(id = id)
    remark_by = school.teacher_set.all()
    log = "teacher"
    id_num = request.user.teacher.id
  elif(request.user.groups.all()[0].name == "non-staff"):
    id = request.user.nonstaff.school.id
    school = School.objects.get(id = id)
    remark_by = school.nonstaff_set.all()
    log = "non-staff"
    id_num = request.user.nonstaff.id
  student = school.student_set.all()
  

  RemarksForm = inlineformset_factory(School, Remark, fields=('name','student','grade','remarks'), extra = 1)
  formset = RemarksForm(queryset = Remark.objects.none(), instance=school)

  if(request.method == 'POST'):
    formset = RemarksForm(request.POST, instance = school)
    form_by = formset.cleaned_data[0].get('name')
    form_on = formset.cleaned_data[0].get('student')
    form_on_grade = formset.cleaned_data[0].get('grade')
    for i in student.filter(name = form_on):
      print(i.name)
    print(student.filter(name = form_on)[0].grade)
    if(formset.is_valid()):
      if(form_by is None or form_on is None or form_on_grade is None):
        messages.error(request, 'Fill all the fields')
      elif(student.filter(name = form_on) is None):
        messages.error(request, f'{form_on} not in databse')
      elif(remark_by.filter(name = form_by) is None):
        messages.error(request, f'{form_by} not in database')
      elif(student.filter(name = form_on)[0].grade != form_on_grade):
        messages.error(request, f'{form_on} does not belong to grade {form_on_grade}')
      else:
        formset.save()
        return redirect('/')
    
  context = {
    "formset": formset,
    "log": log,
    "school": school,
    "id": id_num,
  }

  return render(request, "remarks.html", context = context)
    
        
def remark_display_view(request):
  id = ""
  remarks = Remark.objects.all()
  context = {}
  if request.user.groups.all()[0].name=="school":
    remarks = Remark.objects.all()
    my_filter = AllRemarksFilter(request.GET, queryset = remarks)
    log = "school"
    school = request.user.school
  
  if request.user.groups.all()[0].name=="student":
    remarks = Remark.objects.filter(student = request.user.student.name).filter(grade = request.user.student.grade)
    my_filter = StudentRemarksFilter(request.GET, queryset = remarks)
    log = "student"
    id = request.user.student.id
    school = request.user.student.school

  remarks_list = my_filter.qs

  paginator = Paginator(remarks_list, 10)
  page_number = request.GET.get('page',1)
  page = paginator.get_page(page_number)


  context = {
    "my_filter": my_filter,
    "paginator_range": paginator.get_elided_page_range(number = page_number),
    "page": page,
    "log": log,
    "school": school,
    "id": id,
  }

  return render(request,"remarks-display.html", context = context)