# Generated by Django 4.2.6 on 2023-10-16 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_faculty_options_alter_group_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='projects_num',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tasks_num',
        ),
        migrations.AlterField(
            model_name='user',
            name='biography',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
