from typing import List
from django.contrib.auth.models import User
import django_filters
from . models import *
import floppyforms
# from .views import *

class ProductFilter(django_filters.FilterSet):
    name_of_task = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = AddTask
        fields = ['name_of_task']

      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sample_name_val = AddTask.objects.values_list('name_of_task')
        SAMPLE_NAME_CHOICES = []
    
        query_data =kwargs["queryset"]  
        for data in query_data:
            SAMPLE_NAME_CHOICES.append(data)         
        self.filters['name_of_task'].extra.update({'widget': floppyforms.widgets.Input(datalist=SAMPLE_NAME_CHOICES)})

    