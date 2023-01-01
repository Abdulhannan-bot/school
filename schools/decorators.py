from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_function):
  def wrapper_function(request, *args, **kwargs):
    if request.user.is_authenticated:
      if(request.user.groups.all()[0].name == "teacher"):
        return redirect('school',id = request.user.teacher.school.id)
      elif(request.user.groups.all()[0].name == "student"):
        return redirect('school',id = request.user.student.school.id)
      elif(request.user.groups.all()[0].name == "non-staff"):
        return redirect('school',id = request.user.nonstaff.school.id)
      elif(request.user.groups.all()[0].name == "school"):
        return redirect('school',id = request.user.school.id)
      elif (request.user.groups.all()[0].name == 'admin'):
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
        return redirect('login')
    return wrapper_func
        
# def school_only(view_function):
#   def wrapper_func(request, id, *args, **kwargs):
#     group = None
#     if(request.user.groups.exists()):
#       group = request.user.groups.all()[0].name

#     if(group == 'school'):
#       return view_function(request, id, *args, **kwargs)
      
#     elif(group == 'student'):
#       return redirect('school',id = request.user.student.school.id)
    
#     elif(group == 'teacher'):
#       return redirect('school',id = request.user.teacher.school.id)
    
#     elif(group == 'nonstaff'):
#       return redirect('school',id = request.user.nonstaff.school.id)
    
#     elif(group == 'admin'):
#       return redirect('home')
    
#     else:
#       return redirect('login')
        

#     return wrapper_func

def allowed_users(allowed_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      group = None
      if(request.user.groups.exists()):
        group = request.user.groups.all()[0].name

      if(group in allowed_roles):
        return view_func(request,*args,**kwargs)
      else:
        return HttpResponse('You are not authorized to view this page')

    return wrapper_func
  return decorator