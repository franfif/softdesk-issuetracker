from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from issues.serializers import ProjectSerializer

from issues.models import Project, ProjectContributor


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # if admin, return all projects
        # else, return user's projects
        if self.request.user == 'AnonymousUser':
            print('no user')
            return Project.objects.all()
        print('user is logged in', self.request.user)
        return Project.objects.filter(contributors=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save()
        project.contributors.add(self.request.user,
                                 through_defaults={'role': 'Owner'})
