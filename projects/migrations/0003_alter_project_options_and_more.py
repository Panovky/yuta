# Generated by Django 4.2.6 on 2023-10-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_column_projectcolumn'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name'], 'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.RenameField(
            model_name='project',
            old_name='manager_id',
            new_name='manager',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='team_id',
            new_name='team',
        ),
        migrations.RenameField(
            model_name='projectcolumn',
            old_name='column_id',
            new_name='column',
        ),
        migrations.RenameField(
            model_name='projectcolumn',
            old_name='project_id',
            new_name='project',
        ),
        migrations.AlterField(
            model_name='project',
            name='creation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
