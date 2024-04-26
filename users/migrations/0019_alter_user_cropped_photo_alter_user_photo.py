# Generated by Django 4.2.6 on 2023-10-30 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_user_cropped_photo_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cropped_photo',
            field=models.ImageField(blank=True, default='images/cropped-default-user-photo.png', upload_to='images/users_photos'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='images/default-user-photo.png', upload_to='images/users_photos'),
        ),
    ]
