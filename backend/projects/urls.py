from django.urls import path
from .views import ProjectListCreateView, ProjectMemberListCreateView

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="Project-list-create"),
    path(
        "<int:project_id>/members/",
        ProjectMemberListCreateView.as_view(),
        name="project-members",
    ),
]