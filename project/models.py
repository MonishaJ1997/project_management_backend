from django.db import models
from django.contrib.auth.models import User


# ===============================
# 🔹 PROJECT MODEL
# ===============================
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ===============================
# 🔹 TASK MODEL
# ===============================
class Task(models.Model):

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tasks"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ===============================
# 🔹 ACTIVITY LOG (IMPORTANT 🔥)
# ===============================
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"


# ===============================
# 🔹 NOTIFICATION (OPTIONAL 🔥)
# ===============================
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


# ===============================
# 🔹 SPRINT (ADVANCED - JIRA FEATURE 🔥)
# ===============================
class Sprint(models.Model):
    name = models.CharField(max_length=200)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sprints"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name