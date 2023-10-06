# Generated by Django 4.2.6 on 2023-10-06 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('technical_task', models.FileField(blank=True, null=True, upload_to='')),
                ('creation_date', models.DateField()),
                ('deadline', models.DateField()),
                ('manager_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
                ('team_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teams.team')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
