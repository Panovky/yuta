from rest_framework import serializers
from .models import Project
from users.serializers import ShortUserSerializer
from teams.serializers import TeamSerializer


class ProjectSerializer(serializers.ModelSerializer):
    manager = ShortUserSerializer()
    team = TeamSerializer()

    class Meta:
        model = Project
        fields = ['id', 'photo', 'name', 'technical_task', 'status', 'string_deadline', 'description', 'manager', 'team']