# Generated by Django 4.2.6 on 2023-11-27 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_alter_team_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
