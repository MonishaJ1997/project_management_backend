from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Project, Task,  Sprint
from .models import Project, Task, Sprint, Member

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

        user = User.objects.create_user(**validated_data)
        user.first_name = name
        user.save()

        return user


# =========================================
# 👤 USER SERIALIZER (FOR DROPDOWN)
# =========================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


# =========================================
# 📁 PROJECT SERIALIZER
# =========================================
class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


# =========================================
# 🔄 SPRINT SERIALIZER
# =========================================
class SprintSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        source="project.name",
        read_only=True
    )

    class Meta:
        model = Sprint
        fields = "__all__"


# =========================================
# ✅ TASK SERIALIZER (FULLY FIXED 🔥)
# =========================================

from rest_framework import serializers
from .models import Task, Member

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        allow_null=True,
        required=False
    )

    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"

    def get_assigned_to_name(self, obj):
        return obj.assigned_to.name if obj.assigned_to else None


from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"