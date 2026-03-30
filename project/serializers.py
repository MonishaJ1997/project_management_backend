
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Project, Task, ActivityLog, Notification, Sprint


# =========================================
# 🔐 REGISTER SERIALIZER
# =========================================
class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        name = validated_data.pop('name')

        # ✅ CREATE USER
        user = User.objects.create_user(**validated_data)

        # ✅ SAVE NAME AS first_name
        user.first_name = name
        user.save()

        return user


# =========================================
# 📁 PROJECT SERIALIZER
# =========================================
class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


# =========================================
# ✅ TASK SERIALIZER
# =========================================
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "project",
            "assigned_to",
            "created_at"
        ]

        # 🔥 IMPORTANT: USER AUTO ASSIGNED
        read_only_fields = ["assigned_to"]


# =========================================
# 🔄 SPRINT SERIALIZER
# =========================================
class SprintSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        source='project.name',
        read_only=True
    )

    class Meta:
        model = Sprint
        fields = '__all__'


# =========================================
# 📜 ACTIVITY LOG SERIALIZER
# =========================================
class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ActivityLog
        fields = '__all__'


# =========================================
# 🔔 NOTIFICATION SERIALIZER
# =========================================
class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'