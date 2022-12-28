from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_function):
  def wrapper_function(request, *args, **kwargs):
    if request.user.is_authenticated:
      if(request.user.groups.all()[0].name in ['school','teacher','student','non-staff']):
        print(f'post auth {request.user.groups.all()[0].name}')
        return redirect('school',id = request.user.school.id)
      elif (request.user.groups.all()[0].name == 'admin'):
        print(f'post auth {request.user.groups.all()[0].name}')
        return redirect('home')
      else:
        print('passes through all')
        return view_function(request, *args, **kwargs)
    else:
      return view_function(request, *args, **kwargs)
  return wrapper_function

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
      group = None
      if(request.user.groups.exists()):
        group = request.user.groups.all()[0].name

      if(group == 'admin'):
        return view_func(request, *args, **kwargs)
        
      elif(group == 'student'):
        return redirect('school',id = request.user.student.school.id)
      
      elif(group == 'teacher'):
        return redirect('school',id = request.user.teacher.school.id)
      
      elif(group == 'nonstaff'):
        return redirect('school',id = request.user.nonstaff.school.id)
      
      else:
        return HttpResponse('<p>You are not authorized to use this page</p>')
        

    return wrapper_func
        