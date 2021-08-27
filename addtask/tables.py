import django_tables2 as tables
from floppyforms import fields
from todoapp.models import AddTask

class CompleteTable(tables.Table):
    delete = tables.TemplateColumn(template_name='delete_icon.html')
    complete=tables.TemplateColumn(template_name='complete_success.html')
    class Meta:
        model = AddTask
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("name_of_task","create_date","end_date","create_time","end_time")

class CompleteTask(tables.Table):

    class Meta:
        model=AddTask
        template_name = "django_tables2/bootstrap-responsive.html"
        fields=("name_of_task","create_date","end_date","create_time","end_time")

class PendingTask(tables.Table):

    class Meta:
        model=AddTask
        template_name = "django_tables2/bootstrap-responsive.html"
        fields=("name_of_task","create_date","end_date","create_time","end_time")