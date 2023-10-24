from django.db import models
from users.models import User


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ["name"]

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Участник команды'
        verbose_name_plural = 'Участники команды'
