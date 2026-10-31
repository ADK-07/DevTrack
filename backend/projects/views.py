from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Project, ProjectMembership
from .serializers import ProjectSerializer, ProjectMembershipSerializer

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
        
        
User = get_user_model()        
class ProjectMemberListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_project(self, project_id, user):
        try:
            return Project.objects.get(id=project_id,owner=user)
        except Project.DoesNotExist:
            raise PermissionDenied("You are not allowed to manage this project.")
        
    def get(self, request, project_id):
        project = self.get_project(project_id, request.user)
        
        memberships = ProjectMembership.objects.filter(
            project=project,
        ).select_related("user")
        
        serializer = ProjectMemberListCreateView(
            memberships,
            many=True,
        )
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, project_id):
        project = self.get_project(project_id, request.user)
        
        user_id = request.data.get("user")
        
        if not user_id:
            return Response(
                 {"user": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        try:
            member = User.objects.get(
                id=user_id,
                role="developer",
            )
        except User.DoesNotExist:
            return Response(
                {"user": ["Developer account not found."]},
                status=status.HTTP_404_NOT_FOUND,
            )
            
        if ProjectMembership.objects.filter(
            project=project,
            user=member
        ).exists():
            return Response(
                {"detail": "User is already a project member."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        membership =ProjectMembership.objects.create(
            project=project,
            user=member,
            role=ProjectMembership.Role.DEVELOPER,
        )
        
        serializer = ProjectMembershipSerializer(membership)
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
    
# Create your views here.
