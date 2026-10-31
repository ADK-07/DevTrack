from django.db import models
from django.contrib import settings

from projects.models import Project


class Task(models.Model):
    
    class Priority:
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"
        
    class Status:
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In_Progress"
        DEVELOPED = "developed", "Developed"
        TESTING = "testing", "Testing"
        DEPLOYED = "deployed", "Deployed"
        
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name = "tasks"
    )
    
    titel = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_tasks",
    )
        
        
    

# Create your models here.
