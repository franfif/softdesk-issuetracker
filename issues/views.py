from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from .mixins import ProductQuerySetMixin
from .models import Project, Issue, Comment

from issues.models import Project, ProjectContributor

class ProjectListAPIView(
        ProductQuerySetMixin,
        generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    allow_staff_view = True

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     user = self.request.user
    #     if user.is_staff:
    #         return qs
    #     return qs.filter(contributors=user)

    # def perform_create(self, serializer):
    #     project = serializer.save()
    #     project.contributors.add(self.request.user,
    #                              through_defaults={'role': 'Owner'})


class ProjectDetailAPIView(
        ProductQuerySetMixin,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # def perform_update(self, serializer):
    #     project = serializer.save()
    #     project.contributors.add()


class IssueListAPIView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        if self.kwargs.get('project_pk'):
            return self.queryset.filter(project_id=self.kwargs.get('project_pk'))
        return self.queryset.all()


class IssueDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_object(self):
        if self.kwargs.get('project_pk'):
            return generics.get_object_or_404(self.get_queryset(),
                                              project_id=self.kwargs.get('project_pk'),
                                              pk=self.kwargs.get('issue_pk'))
        else:
            return generics.get_object_or_404(self.get_queryset(),
                                              pk=self.kwargs.get('issue_pk'))


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_object(self):
        if self.kwargs.get('project_pk') and self.kwargs.get('issue_pk'):
            print('there is an issue_pk')
            return generics.get_object_or_404(self.get_queryset(),
                                              project_id=self.kwargs.get('project_pk'),
                                              issue_id=self.kwargs.get('issue_pk'))
            # project_id=self.kwargs.get('project_pk'),
        print('there is no issue pk')
        return self.queryset.all()


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_object(self):
        if self.kwargs.get('project_pk') and self.kwargs.get('issue_pk'):
            return generics.get_object_or_404(self.get_queryset(),
                                              issue_id=self.kwargs.get('issue_pk'),
                                              pk=self.kwargs.get('comment_pk'))
        else:
            return generics.get_object_or_404(self.get_queryset(),
                                              pk=self.kwargs.get('comment_pk'))


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
