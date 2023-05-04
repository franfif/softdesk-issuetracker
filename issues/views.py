from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from . import mixins
from .models import Project, Issue, Comment, Contributor


class ProjectListAPIView(
        mixins.ProductQuerySetMixin,
        generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    allow_staff_view = True

    # def perform_create(self, serializer):
    #     project = serializer.save()
    #     project.contributors.add(self.request.user,
    #                              through_defaults={'role': 'Owner'})


class ProjectDetailAPIView(
        mixins.ProductQuerySetMixin,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # def perform_update(self, serializer):
    #     project = serializer.save()
    #     project.contributors.add()


class IssueListAPIView(
        mixins.MultipleFieldListViewMixin,
        generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_fields = ['project_id']

    def perform_create(self, serializer):
        issue = serializer.save(project=Project.objects.get(id=self.kwargs.get('project_id')),
                                author=self.request.user)
        if not issue.assignee:
            issue.assignee = self.request.user


class IssueDetailAPIView(
        mixins.MultipleFieldDetailViewMixin,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_fields = ['project_id', 'id']


class CommentListAPIView(
        mixins.MultipleFieldListViewMixin,
        generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_fields = ['project_id', 'issue_id']

    # Need to check if the user is authorized to access the project
    # And that the comment belongs to the project.

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs.get('issue_id'))
        serializer.save(issue=issue,
                        project=issue.project,
                        author=self.request.user)


class CommentDetailAPIView(
        mixins.MultipleFieldDetailViewMixin,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_fields = ['project_id', 'issue_id', 'id']


class ContributorListAPIView(
        mixins.MultipleFieldListViewMixin,
        generics.ListCreateAPIView):
    # queryset = Contributor.objects.filter(project=self.kwargs.get('project_pk'))
    queryset = Contributor.objects.all()

    serializer_class = ContributorSerializer
    lookup_fields = ['project_id']

    def perform_create(self, serializer):
        project = generics.get_object_or_404(Project,
                                             id=self.kwargs.get('project_pk'))
        # user = self.kwargs.get('user')
        serializer.save(project=project,
                        # user=user,
                        role=Contributor.CONTRIBUTOR)


class ContributorDestroyAPIView(
        mixins.MultipleFieldDetailViewMixin,
        generics.DestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    lookup_fields = ['project_id', 'id']


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
