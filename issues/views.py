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

# class ProjectViewSet(ModelViewSet):
#     serializer_class = ProjectSerializer
#
#     # permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         # if admin, return all projects
#         # else, return user's projects
#         if self.request.user.is_staff:
#             return Project.objects.all()
#         # For now, return all projects if user is not authenticated
#         # return Project.objects.filter(contributors=self.request.user)
#         return Project.objects.all()
#
#     def perform_create(self, serializer):
#         project = serializer.save()
#         # For now, allow creation if user is not authenticated
#         # project.contributors.add(self.request.user,
#         #                          through_defaults={'role': 'Owner'})


# class ContributorViewSet(ModelViewSet):
#     serializer_class = ContributorSerializer
#     queryset = Contributor.objects.all()
#
#     def get_queryset(self, pk=None):
#         if pk is not None:
#             return ProjectContributor.objects.filter(project=pk)
#         return ProjectContributor.objects.all()
