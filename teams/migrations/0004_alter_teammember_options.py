# Generated by Django 4.2.6 on 2023-10-24 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_remove_team_leader'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teammember',
            options={'verbose_name': 'Участник команды', 'verbose_name_plural': 'Участники команды'},
        ),
    ]
