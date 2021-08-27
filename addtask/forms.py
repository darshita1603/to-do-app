from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from todoapp.models import *

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = AddTask
        fields = ["user","name_of_task","end_date","end_time"]

