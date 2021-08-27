import django_tables2 as tables
from django.shortcuts import redirect, render,get_object_or_404
from .models import AddTask
from datetime import date


def task_due_date_color_for_row(**kwargs):
    row = kwargs.get("record",None)
    # taskid = row.pk
    date1 = row.end_date
    date2 = date.today()
    diff_date=(date1-date2).days
    if diff_date<0:
        return "color:red;"
    elif diff_date<2:
        return "color:blue;"
    else:
        return 'color:black;'


class PersonTable(tables.Table):
    Edit = tables.TemplateColumn(template_name='table_task_edit_btn.html')
    delete = tables.TemplateColumn(template_name='delete_icon.html')
    pdf=tables.TemplateColumn(template_name='downloadpdf_icon.html')
    complete=tables.TemplateColumn(template_name='complete_icon.html')
    class Meta:
            row_attrs = {
            "style": task_due_date_color_for_row
        }
            model = AddTask
            template_name = "django_tables2/bootstrap-responsive.html"
            fields = ("user_id","name_of_task","create_date","end_date","create_time","end_time")

