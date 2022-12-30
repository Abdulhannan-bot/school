from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


GRADE = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
  )

class School(models.Model):
  user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
  name = models.CharField(max_length = 50, null = True, blank = True)
  phone = models.CharField(max_length = 20, null=True)
  email = models.CharField(max_length = 50, null=True)
  profile_pic = models.ImageField(default="img1.jpg", null=True, blank=True)

  def __str__(self):
    return str(self.name)


class Teacher(models.Model):
  user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
  name = models.CharField(max_length = 50, null = True, blank = True)
  phone = models.CharField(max_length = 20, null=True)
  email = models.CharField(max_length = 50, null=True)
  school = models.ForeignKey(School, null = True, on_delete = models.CASCADE)
  grade = models.CharField(max_length = 2, null = True, choices = GRADE)

  def __str__(self):
    return str(self.school)+" - teacher"
  
class Student(models.Model):
  user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
  name = models.CharField(max_length = 50, null = True, blank = True)
  phone = models.CharField(max_length = 20, null=True)
  email = models.CharField(max_length = 50, null=True)
  school = models.ForeignKey(School, null = True, on_delete = models.CASCADE)
  grade = models.CharField(max_length = 2, null = True, choices = GRADE)

  def __str__(self):
    return str(self.school)+" - student"

class NonStaff(models.Model):
  DESIGNATION = [
    ('counsellor', 'counsellor'),
    ('principal', 'principal'),
    ('vice principal', 'vice principal'),
    ('office','office'),
    ('reciptionist','reciptionist'),
  ]
  user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
  name = models.CharField(max_length = 50, null = True, blank = True)
  phone = models.CharField(max_length = 20, null=True)
  email = models.CharField(max_length = 50, null=True)
  school = models.ForeignKey(School, null = True, on_delete = models.CASCADE)
  designation = models.CharField(max_length = 20, null = True, choices = DESIGNATION)

class Remark(models.Model):
  # user = models.ForeignKey(Group, null = True, on_delete = models.CASCADE)
  name = models.CharField(max_length = 50, null = True)
  school = models.ForeignKey(School, null = True, on_delete = models.CASCADE)
  student = models.CharField(max_length = 50, null = True)
  grade = models.CharField(max_length = 2, null = True, choices = GRADE)
  remarks = models.CharField(max_length = 200, null = True)
  

def create_user(sender, instance, created, **kwargs):
  def make_title(name):
    name = name.lower()
    name = name[0].upper()+name[1:]
    return name

  def group_adder(name,str,group_name,Class, school_check = False):
    name_clone = name
    name = name.replace(str,"")
    name = list(map(make_title,name.split("-")))
    name = " ".join(name)
    if(Class.objects.filter(name = name).exists):
      Class.objects.filter(name = name).update(user = User.objects.get(username = name_clone))
    else:
      Class.objects.create(user = instance, name = name)
    group = Group.objects.get(name = group_name)
    instance.groups.add(group)
  
  def check_username(name):
    if name.startswith("std_user-"):
      group_adder(name,"std_user-","student",Student)
    elif name.startswith("staff_user-"):
      group_adder(name,"staff_user-","teacher",Teacher)
    elif name.startswith("nstaff_user-"):
      group_adder(name,"nstaff_user-","non-staff",NonStaff)
    elif name.startswith("school_user-"):
      group_adder(name,"school_user-","school",School)

  if created:
    name = instance.username
    check_username(name)

post_save.connect(create_user, sender = User)


@receiver(post_save, sender = Student)
@receiver(post_save, sender = Teacher)
@receiver(post_save, sender = NonStaff)
@receiver(post_save, sender = School)
def user_create(sender, instance, created, **kwargs):
  def generate(str):
    name = instance.name
    name = name.lower().split(" ")
    name = "-".join(name)
    User.objects.create(username = f'{str}-{name}')
  if(created and sender == Student):
    generate('std_user')
  elif(created and sender == Teacher):
    generate('staff_user')
  elif(created and sender == NonStaff):
    generate('nstaff_user')
  elif(created and sender == School):
    generate('school_user')
    

    # sender.objects.get(name = name).user = User.objects.create(username = 'std_user-'+name1)
