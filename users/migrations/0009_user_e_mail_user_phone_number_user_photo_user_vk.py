# Generated by Django 4.2.6 on 2023-10-18 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_patronymic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='e_mail',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/users_photos'),
        ),
        migrations.AddField(
            model_name='user',
            name='vk',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
