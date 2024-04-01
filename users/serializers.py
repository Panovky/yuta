from rest_framework import serializers
from .models import User


class FullUserSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField()
    direction = serializers.StringRelatedField()
    group = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['photo', 'cropped_photo', 'last_name', 'first_name', 'patronymic', 'age', 'biography',
                  'phone_number', 'e_mail', 'vk', 'faculty', 'direction', 'group', 'all_projects_count',
                  'done_projects_count', 'all_tasks_count', 'done_tasks_count', 'teams_count']


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'cropped_photo', 'last_name', 'first_name', 'patronymic']