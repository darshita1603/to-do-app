from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

# Create your models here.

class Registration(models.Model):
    email=models.EmailField()
    username=models.CharField(max_length=255)
    password = models.CharField(default="",max_length=50)
    mobileno=models.PositiveIntegerField(null=True,default=0)
    image=models.ImageField(default='/profile_pics/default.jpg',upload_to='profile_pics')
    about=models.CharField(default="",max_length=255) 
    dateofbirth=models.DateField(default="2012-09-04", blank=True)


    def __str__(self):
        return self.username

class AddTask(models.Model):
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    name_of_task=models.CharField(max_length=255)
    details=models.TextField()
    create_date=models.DateField(auto_now_add=True)
    end_date=models.DateField()
    create_time=models.TimeField(auto_now_add=True)
    end_time=models.TimeField()
    complete=models.BooleanField(default=False)

    def __str__(self):
        return self.name_of_task
