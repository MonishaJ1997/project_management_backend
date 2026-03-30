

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Project, Task, Sprint, ActivityLog, Notification
from .serializers import (
    RegisterSerializer,
    ProjectSerializer,
    TaskSerializer,
    SprintSerializer,
    ActivityLogSerializer,
    NotificationSerializer
)

# =========================================
# 🔐 LOGIN
# =========================================
@api_view(['POST'])
def login(request):
    email = request.data.get("username")  # frontend sends email
    password = request.data.get("password")

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email"}, status=400)

    user = authenticate(username=user_obj.username, password=password)

    if user is None:
        return Response({"error": "Invalid password"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })


# =========================================
# 📝 REGISTER
# =========================================
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created"})

    return Response(serializer.errors, status=400)


# =========================================
# 👤 CURRENT USER
# =========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    return Response({
        "username": user.username,
        "name": user.first_name
    })


# =========================================
# 📊 DASHBOARD
# =========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user

    tasks = Task.objects.filter(assigned_to=user)
    projects = Project.objects.filter(created_by=user)

    data = {
        "username": user.username,
        "total_tasks": tasks.count(),
        "todo": tasks.filter(status="todo").count(),
        "in_progress": tasks.filter(status="in_progress").count(),
        "done": tasks.filter(status="done").count(),
        "total_projects": projects.count(),
    }

    return Response(data)


# =========================================
# 📁 PROJECT APIs
# =========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def projects(request):

    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# =========================================
# ✅ TASK APIs
# =========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tasks(request):

    if request.method == 'GET':
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(assigned_to=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# =========================================
# ✏️ UPDATE / DELETE TASK
# =========================================
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_task(request, pk):

    try:
        task = Task.objects.get(id=pk, assigned_to=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            updated_task = serializer.save()

            ActivityLog.objects.create(
                user=request.user,
                action=f"Updated task '{updated_task.title}'",
                task=updated_task
            )

            return Response(serializer.data)

    if request.method == 'DELETE':
        task_title = task.title
        task.delete()

        ActivityLog.objects.create(
            user=request.user,
            action=f"Deleted task '{task_title}'"
        )

        return Response({"message": "Task deleted"})


# =========================================
# 🔄 SPRINTS
# =========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sprints(request):

    if request.method == 'GET':
        data = Sprint.objects.all()
        serializer = SprintSerializer(data, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SprintSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


# =========================================
# 📜 ACTIVITY LOGS
# =========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_logs(request):
    logs = ActivityLog.objects.all().order_by('-timestamp')
    serializer = ActivityLogSerializer(logs, many=True)
    return Response(serializer.data)


# =========================================
# 🔔 NOTIFICATIONS
# =========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications(request):
    data = Notification.objects.filter(user=request.user)
    serializer = NotificationSerializer(data, many=True)
    return Response(serializer.data)