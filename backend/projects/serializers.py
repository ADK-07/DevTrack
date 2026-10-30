from rest_framework import serializers

from .models import Project

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