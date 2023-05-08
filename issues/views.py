from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .models import Project, Issue, Comment, Contributor


class ProjectListAPIView(
        generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        if self.allow_staff_view:
            print(self.allow_staff_view)
            return Project.objects.all()
        queryset = Project.objects.filter(contributors__user=self.request.user)
        return queryset


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer

    def get_object(self):
        print(self.request.user)
        print(self.kwargs.get('id'))
        print(Project.objects.filter(contributors__user=self.request.user,
                                     id=self.kwargs.get('id')))
        obj = generics.get_object_or_404(Project,
                                         contributors__user=self.request.user,
                                         id=self.kwargs.get('id'))
        return obj


class IssueListAPIView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.filter(project=self.kwargs.get('project_id'))
        return queryset

    def perform_create(self, serializer):
        issue = serializer.save(project=Project.objects.get(id=self.kwargs.get('project_id')),
                                author=self.request.user)
        if not issue.assignee:
            issue.assignee = self.request.user


class IssueDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer

    def get_object(self):
        obj = generics.get_object_or_404(Issue,
                                         project=self.kwargs.get('project_id'),
                                         id=self.kwargs.get('id'))
        return obj


class CommentListAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(issue__project=self.kwargs.get('project_id'),
                                          issue=self.kwargs.get('issue_id'))
        return queryset

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs.get('issue_id'))
        serializer.save(issue=issue,
                        project=issue.project,
                        author=self.request.user)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_fields = ['project_id', 'issue_id', 'id']

    def get_object(self):
        obj = generics.get_object_or_404(Comment,
                                         issue__project=self.kwargs.get('project_id'),
                                         issue=self.kwargs.get('issue_id'),
                                         id=self.kwargs.get('id'))
        return obj


class ContributorListAPIView(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Contributor.objects.filter(project=self.kwargs.get('project_id'))
        return queryset

    def perform_create(self, serializer):
        project = generics.get_object_or_404(Project,
                                             id=self.kwargs.get('project_id'))
        serializer.save(project=project,
                        role=Contributor.CONTRIBUTOR)


class ContributorDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ContributorSerializer

    def get_object(self):
        obj = generics.get_object_or_404(Contributor,
                                         project=self.kwargs.get('project_id'),
                                         id=self.kwargs.get('id'))
        return obj

