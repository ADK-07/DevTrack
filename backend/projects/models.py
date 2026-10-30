from django.db import models
from django.conf import settings

class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ARCHIEVED = "archieved", "Archieved"
        
    name = models.CharField(max_length=150)
    key = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_project",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key} - {self.name}"
    
class ProjectMembership(models.Model):
    class Role(models.TextChoices):
        MANAGER = "manager", "Manager"
        DEVELOPER = "developer", "Developer"
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_membership"
    )
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.DEVELOPER,
    )
    
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project","user"],
                name="unique_project_member",
            )
        ]
        
    def __str__(self):
        return f"{self.user.email} - {self.project.key} ({self.role})"

# Create your models here.
