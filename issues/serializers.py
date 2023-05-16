from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'role', 'project']
        read_only_fields = ['user', 'role', 'project']

    def get_user(self, obj):
        user = {'id': obj.user.id,
                'name': obj.user.username}
        return user


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'owner', 'contributors', 'issues']
        read_only_fields = ['owner']

    def get_owner(self, obj):
        return obj.owner.username

    def get_contributors(self, obj):
        names = []
        for contributor in obj.contributors.all():
            names.append(contributor.user.username)
        return names

    def get_issues(self, obj):
        issues = []
        for issue in obj.issue_set.all():
            issues.append({'id': issue.id,
                           'title': issue.title,
                           'tag': issue.tag,
                           'priority': issue.priority,
                           'status': issue.status})
        return issues


class IssueSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'project', 'status', 'author', 'assignee', 'created_time', 'comments']
        read_only_fields = ['project', 'created_time', 'author']

    def get_comments(self, obj):
        comments = []
        for comment in obj.comment_set.all():
            comments.append({'id': comment.id,
                             'description': comment.description,
                             'author': comment.author.username})
        return comments


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
        read_only_fields = ['issue', 'created_time', 'author']
