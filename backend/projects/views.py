from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from .models import Project, ProjectMembership
from .serializers import ProjectSerializer

class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        projects = Project.objects.filter(
            memberships__user = request.user
        ).select_related("owner").distinct()
        
        serializer = ProjectSerializer(projects, many=True)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        if request.user.role != "manager":
            raise PermissionDenied("Only manager can create projects.")
        
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            project = serializer.save(owner=request.user)
            
            ProjectMembership.objects.create(
                project=project,
                user=request.user,
                role=ProjectMembership.Role.MANAGER,
            )
        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_201_CREATED
        )
# Create your views here.
