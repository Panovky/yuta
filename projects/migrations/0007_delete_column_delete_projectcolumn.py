# Generated by Django 4.2.6 on 2023-10-25 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_remove_projectcolumn_column_and_more'),
        ('tasks', '0004_remove_task_column_alter_task_appointed_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Column',
        ),
        migrations.DeleteModel(
            name='ProjectColumn',
        ),
    ]
