from rest_framework import serializers

from .models import Project, ProjectMembership

class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(
        source="owner.full_name",
        read_only=True,
    )
    
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "key",
            "description",
            "owner",
            "owner_name",
            "status",
            "created_at",
            "update_at"
        ]
        read_only_fields = [
            "id",
            "owner",
            "owner_name",
            "created_at",
            "updated_at",
        ]
        
class ProjectMembershipSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.full_name",
        read_only=True
    )
    
    user_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )
    
    class Meta:
        model=ProjectMembership
        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "role",
            "joined_at",
        ]
        
        read_only_fields = [
            "id",
            "user_name",
            "user_email",
            "joined_at",
        ]