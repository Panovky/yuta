# Generated by Django 4.2.6 on 2023-10-19 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='images/default-user-photo.png', null=True, upload_to='images/users_photos'),
        ),
    ]
