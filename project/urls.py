from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    register,
    dashboard,
    projects,
    tasks,
    update_task,
    sprints,
    activity_logs,
    notifications
)

from django.urls import path
from .views import me

urlpatterns = [
    path('me/', me),   # ✅ THIS IS IMPORTANT

    # 🔐 AUTH
    path('register/', register),
    path('login/', TokenObtainPairView.as_view()),  # JWT login

    # 📊 DASHBOARD
    path('dashboard/', dashboard),

    # 📁 PROJECT
    path('projects/', projects),

    # ✅ TASK
    path('tasks/', tasks),
    path('tasks/<int:pk>/', update_task),

    # 🔄 SPRINT
    path('sprints/', sprints),

    # 📜 ACTIVITY
    path('activity/', activity_logs),

    # 🔔 NOTIFICATIONS
    path('notifications/', notifications),
]