import django_tables2 as tables
from .models import AddTask

class PersonTable(tables.Table):
    Edit = tables.TemplateColumn(template_name='table_task_edit_btn.html')
    delete = tables.TemplateColumn(template_name='delete_icon.html')
    complete=tables.TemplateColumn(template_name='complete_icon.html')
    class Meta:
        model = AddTask
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("user_id","name_of_task","create_date","end_date","create_time","end_time")