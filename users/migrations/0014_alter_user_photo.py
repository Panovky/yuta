# Generated by Django 4.1.4 on 2023-10-24 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_user_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='images/default_user_photo.png', upload_to='images/users_photos'),
        ),
    ]
