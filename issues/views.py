from rest_framework import generics, permissions

from .permissions import IsProjectOwnerOrReadOnly, IsProjectContributor, IsAuthorOrReadOnly
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .models import Project, Issue, Comment, Contributor


class ProjectListAPIView(
        generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    # Any authenticated user should be able to create a project
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        # A user can only see the projects for which they are a contributor
        queryset = Project.objects.filter(contributors__user=self.request.user)
        return queryset

    # perform_create() from the view or create() from the serializer?
    def perform_create(self, serializer):
        owner = self.request.user
        project = serializer.save(owner=owner)

        project.contributors.add(Contributor.objects.create(user=owner,
                                                            role=Contributor.OWNER,
                                                            project=project))


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    # Only the owner should be able to update & delete a project
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectOwnerOrReadOnly]

    def get_queryset(self):
        # Only contributors should be able to see a project
        queryset = Project.objects.filter(contributors__user=self.request.user)
        return queryset

    def get_object(self):
        obj = generics.get_object_or_404(self.get_queryset(),
                                         id=self.kwargs.get('id'))
        self.check_object_permissions(self.request, obj)
        return obj


class IssueListAPIView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    # Only contributors should be able to create & read issues on a project
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectContributor]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs.get('project_id'))

    def perform_create(self, serializer):
        project = generics.get_object_or_404(Project,
                                             id=self.kwargs.get('project_id'))

        if 'assignee' in serializer.validated_data:
            assignee = serializer.validated_data.pop('assignee')
            print(assignee)
            # if assignee is not a contributor in project
            # raise ValidationError
            if not Project.objects.filter(id=self.kwargs.get('project_id'),
                                          contributors__user=assignee).exists():
                raise serializers.ValidationError(
                    {'assignee': "The issue's assignee must be a contributor of this project."})
        else:
            assignee = self.request.user

        serializer.save(project=project,
                        author=self.request.user,
                        assignee=assignee)


class IssueDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    # Only the author should be able to update & delete an issue
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectContributor,
                          IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Issue.objects.filter(project=self.kwargs.get('project_id'))
        return queryset

    def get_object(self):
        obj = generics.get_object_or_404(self.get_queryset(),
                                         id=self.kwargs.get('id'))
        return obj

    def perform_update(self, serializer):
        if 'assignee' in serializer.validated_data:
            assignee = serializer.validated_data.pop('assignee')
            # if assignee is not a contributor in project
            # raise ValidationError
            if not Project.objects.filter(id=self.kwargs.get('project_id'),
                                          contributors__user=assignee).exists():
                raise serializers.ValidationError(
                    {'assignee': "The issue's assignee must be a contributor of this project."})
        else:
            assignee = self.request.user

        serializer.save(assignee=assignee)


class CommentListAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    # Only contributors should be able to create & read comments on an issue
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectContributor]

    def get_queryset(self):
        queryset = Comment.objects.filter(issue__project=self.kwargs.get('project_id'),
                                          issue=self.kwargs.get('issue_id'))
        return queryset

    def perform_create(self, serializer):
        issue = generics.get_object_or_404(Issue,
                                           id=self.kwargs.get('issue_id'))
        serializer.save(issue=issue,
                        author=self.request.user)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    # Only the author should be able to update & delete a comment
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectContributor,
                          IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(issue__project=self.kwargs.get('project_id'),
                                          issue=self.kwargs.get('issue_id'))
        return queryset

    def get_object(self):
        obj = generics.get_object_or_404(self.get_queryset(),
                                         id=self.kwargs.get('id'))
        return obj


class ContributorListAPIView(generics.ListCreateAPIView):
    serializer_class = ContributorSerializer
    # Only the project owner should be able to add contributors
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectOwnerOrReadOnly]

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
    # Only the project owner should be able to update and delete contributors
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Contributor.objects.filter(project=self.kwargs.get('project_id'))
        return queryset

    def get_object(self):
        obj = generics.get_object_or_404(self.get_queryset(),
                                         user=self.kwargs.get('user_id'))
        return obj
