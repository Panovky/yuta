from django.db import models
from users.models import User


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    leader = models.ForeignKey(User, related_name='leader_teams', null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ["name"]

    def __str__(self):
        return self.name
