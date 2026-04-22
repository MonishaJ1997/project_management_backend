from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import Project, Task, Sprint, Member
from .serializers import (
    RegisterSerializer,
    ProjectSerializer,
    TaskSerializer,
    SprintSerializer,
)

# =========================================
# 🔐 LOGIN (EMAIL BASED)
# =========================================
@api_view(['POST'])
def login(request):
    email = request.data.get("username")
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
        "id": user.id,
        "username": user.username,
        "name": user.first_name
    })


# =========================================
# 👥 USERS
# =========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users(request):
    data = User.objects.all().values("id", "username", "email")
    return Response(data)


# =========================================
# 📊 DASHBOARD
# =========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    tasks = Task.objects.all()
    projects = Project.objects.all()

    return Response({
        "total_tasks": tasks.count(),
        "todo": tasks.filter(status="todo").count(),
        "in_progress": tasks.filter(status="in_progress").count(),
        "done": tasks.filter(status="done").count(),
        "total_projects": projects.count(),
    })


# =========================================
# 📁 PROJECTS
# =========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def projects(request):

    if request.method == 'GET':
        data = Project.objects.all()
        return Response(ProjectSerializer(data, many=True).data)

    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# =========================================
# 📌 TASKS (LIST + CREATE)
# =========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tasks(request):

    if request.method == 'GET':
        data = Task.objects.all()
        return Response(TaskSerializer(data, many=True).data)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# =========================================
# ✏️ TASK DETAIL (UPDATE + DELETE)
# =========================================
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    # ✅ DELETE (handle first)
    if request.method == 'DELETE':
        task.delete()
        return Response({"message": "Task deleted"}, status=204)

    # ✅ PATCH
    if request.method == 'PATCH':
        data = request.data.copy()

        # 🔥 force integer conversion
        if 'assigned_to' in data and data['assigned_to'] not in [None, ""]:
            try:
                data['assigned_to'] = int(data['assigned_to'])
            except:
                data['assigned_to'] = None

        serializer = TaskSerializer(task, data=data, partial=True)

        if serializer.is_valid():
            print("VALID:", serializer.validated_data)
            serializer.save()
            return Response(serializer.data)

        print("ERROR:", serializer.errors)
        return Response(serializer.errors, status=400)
# =========================================
# 📅 SPRINTS
# =========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sprints(request):

    if request.method == 'GET':
        data = Sprint.objects.all()
        return Response(SprintSerializer(data, many=True).data)

    if request.method == 'POST':
        serializer = SprintSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# =========================================
# 🗑 DELETE SPRINT
# =========================================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_sprint(request, pk):

    try:
        sprint = Sprint.objects.get(id=pk)
    except Sprint.DoesNotExist:
        return Response({"error": "Sprint not found"}, status=404)

    sprint.delete()
    return Response({"message": "Sprint deleted"})


# =========================================
# 👥 MEMBERS (NO CSRF)
# =========================================
@csrf_exempt
def members(request):

    if request.method == "GET":
        return JsonResponse(list(Member.objects.values()), safe=False)

    if request.method == "POST":
        body = json.loads(request.body)

        member = Member.objects.create(
            name=body.get("name"),
            role=body.get("role")
        )

        return JsonResponse({
            "id": member.id,
            "name": member.name,
            "role": member.role
        })


# =========================================
# 🗑 MEMBER DELETE
# =========================================
@csrf_exempt
def member_detail(request, pk):

    try:
        member = Member.objects.get(id=pk)
    except Member.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "DELETE":
        member.delete()
        return JsonResponse({"message": "Deleted"})

    return JsonResponse({"error": "Method not allowed"}, status=405)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, pk):
    try:
        project = Project.objects.get(id=pk, created_by=request.user)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)

    project.delete()
    return Response({"message": "Project deleted"})





