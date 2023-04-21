from rest_framework.views import APIView

from issues.serializers import ProjectSerializer

from issues.models import Project


class ProjectViewSet(APIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # if admin, return all projects
        # else, return user's projects
        return Project.objects.filter(contributors=self.request.user)
