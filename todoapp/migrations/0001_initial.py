# Generated by Django 3.2.6 on 2021-08-20 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name_of_task', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('create_time', models.TimeField(auto_now_add=True)),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(default='', max_length=50)),
                ('mobileno', models.PositiveIntegerField(default=0, null=True)),
                ('image', models.ImageField(default='/profile_pics/default.jpg', upload_to='profile_pics')),
                ('about', models.CharField(default='', max_length=255)),
                ('dateofbirth', models.DateField(blank=True, default='2012-09-04')),
            ],
        ),
    ]
