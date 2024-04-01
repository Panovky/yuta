from rest_framework import serializers
from .models import Team
from users.serializers import ShortUserSerializer


class TeamSerializer(serializers.ModelSerializer):
    leader = ShortUserSerializer()
    members = ShortUserSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'leader', 'members']
