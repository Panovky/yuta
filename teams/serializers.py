from rest_framework import serializers
from users.serializers import ShortUserSerializer
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    leader = ShortUserSerializer()
    members = ShortUserSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'leader', 'members']
