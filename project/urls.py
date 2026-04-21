from django.urls import path
from . import views
from .views import (
    register,
    login,              # ✅ use your custom login
    me,
    dashboard,
    projects,
    delete_project,
    tasks,
    task_detail,
    sprints,
    delete_sprint,
    
    users              # ✅ for dropdown
)

urlpatterns = [

    # =========================================
    # 🔐 AUTH
    # =========================================
    path('register/', register),
    path('login/', login),   # ✅ FIXED (use your login)
    path('me/', me),

    # =========================================
    # 👥 USERS
    # =========================================
    path('users/', users),   # 🔥 for assign dropdown

    # =========================================
    # 📊 DASHBOARD
    # =========================================
    path('dashboard/', dashboard),

    # =========================================
    # 📁 PROJECT
    # =========================================
    path('projects/', projects),
    path('projects/<int:pk>/', delete_project),  # ✅ DELETE

    # =========================================
    # ✅ TASK
    # =========================================
    path('tasks/', tasks),
    path("tasks/<int:pk>/", task_detail),

    # =========================================
    # 🔄 SPRINT
    # =========================================
    path('sprints/', sprints),
    path('sprints/<int:pk>/', delete_sprint),  # ✅ DELETE

    # =========================================
    # 📜 ACTIVITY
    # =========================================


     path('members/', views.members),            # GET, POST
    path('members/<int:pk>/', views.member_detail), # DELEte
]