from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

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
  profile_pic = models.ImageField(default="", null=True, blank=True)

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
  # print(School.objects.get(user = "school_user-wisdon-international-school").all())
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

class Remarks(models.Model):
  user = models.ForeignKey(Group, null = True, on_delete = models.CASCADE)
  remarks_on = models.ForeignKey(Student, null = True, on_delete = models.CASCADE)
  

def create_user(sender, instance, created, **kwargs):
  def make_title(name):
    name = name.lower()
    name = name[0].upper()+name[1:]
    return name

  def group_adder(name,str,group_name,Class):
    name = name.replace(str,"")
    name = list(map(make_title,name.split("-")))
    name = " ".join(name)
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