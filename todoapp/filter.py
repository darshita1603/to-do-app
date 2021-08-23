import django_filters
from . models import *

class ProductFilter(django_filters.FilterSet):
    name_of_task = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = AddTask
        fields = ['name_of_task']