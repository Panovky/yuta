import datetime
from django.db import models
from users.models import User
from teams.models import Team
from services.file_path_getter import get_file_path

STATUS_CHOICES = (
    ('в работе', 'в работе'),
    ('приостановлен', 'приостановлен'),
    ('завершен', 'завершен')
)


def get_photo_path(instance, file_name):
    return get_file_path(file_name, 'images/projects_photos')


def get_technical_task_path(instance, file_name):
    return get_file_path(file_name, 'projects_technical_tasks')


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    photo = models.ImageField(blank=True, upload_to=get_photo_path, default='images/project-default-photo.png')
    description = models.CharField(max_length=150)
    technical_task = models.FileField(blank=True, null=True, upload_to=get_technical_task_path)
    creation_date = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='в работе')
    manager = models.ForeignKey(User, related_name='manager_projects', null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, related_name='team_projects', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def string_deadline(self):
        if self.status == 'приостановлен':
            return 'Разработка проекта приостановлена'
        if self.status == 'завершен':
            return 'Проект успешно завершен'

        deadline = self.deadline
        today = datetime.date.today()
        days = (deadline - today).days

        if days < 0:
            return 'Сдача проекта просрочена'
        elif days == 0:
            return 'Срок сдачи проекта: сегодня'
        else:
            return f'Дней до сдачи проекта: {days}'

