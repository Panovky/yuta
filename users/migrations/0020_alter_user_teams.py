# Generated by Django 4.2.6 on 2023-11-03 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_alter_team_members'),
        ('users', '0019_alter_user_cropped_photo_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='teams',
            field=models.ManyToManyField(to='teams.team'),
        ),
    ]
