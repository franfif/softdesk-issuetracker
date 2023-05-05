from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from . import mixins
from .models import Project, Issue, Comment, Contributor


class ProjectListAPIView(
        mixins.ProductQuerySetMixin,
        generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    allow_staff_view = False


class ProjectDetailAPIView(
        mixins.ProductQuerySetMixin,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


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
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    lookup_fields = ['project_id']

    def perform_create(self, serializer):
        project = generics.get_object_or_404(Project,
                                             id=self.kwargs.get('project_id'))
        serializer.save(project=project,
                        role=Contributor.CONTRIBUTOR)


class ContributorDestroyAPIView(
        mixins.MultipleFieldDetailViewMixin,
        generics.DestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    lookup_fields = ['project_id', 'id']
