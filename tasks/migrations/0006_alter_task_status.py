# Generated by Django 4.2.6 on 2023-10-30 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('назначена', 'назначена'), ('в работе', 'в работе'), ('выполнена', 'выполнена')], max_length=20, null=True),
        ),
    ]
