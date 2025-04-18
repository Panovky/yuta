# Generated by Django 4.2.6 on 2024-03-14 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='creation_datetime',
        ),
        migrations.AddField(
            model_name='task',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('сделать', 'сделать'), ('в работе', 'в работе'), ('на проверке', 'на проверке'), ('готово', 'готово'), ('на стопе', 'на стопе')], max_length=20),
        ),
    ]
