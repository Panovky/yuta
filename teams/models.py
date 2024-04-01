from django.db import models
from users.models import User


class TeamQuerySet(models.query.QuerySet):
    def create_team(self, **kwargs):
        team = self.create(
            name=kwargs['name'],
            leader_id=kwargs['leader_id']
        )
        for member_id in kwargs['members_id']:
            member = User.objects.get(id=member_id)
            team.members.add(member)
            member.teams.add(team)

    def update_team(self, **kwargs):
        team = Team.objects.get(id=kwargs['id'])
        team.name = kwargs['name']
        team.members.clear()
        for member_id in kwargs['members_id']:
            member = User.objects.get(id=member_id)
            team.members.add(member)
            member.teams.add(team)
        team.save()


class BaseTeamManager(models.Manager):
    pass


class TeamManager(BaseTeamManager.from_queryset(TeamQuerySet)):
    pass


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    leader = models.ForeignKey(User, related_name='leader_teams', null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User)

    objects = TeamManager()

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ["name"]

    def __str__(self):
        return self.name
