from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment


# Project Serializers
class ProjectListSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'owner']

    def get_owner(self, obj):
        return obj.owner.username


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'owner']
        read_only_fields = ['owner']


class ProjectDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'owner', 'contributors', 'issues']
        read_only_fields = ['owner']

    def get_owner(self, obj):
        return {'id': obj.owner.id,
                'username': obj.owner.username}

    def get_contributors(self, obj):
        contributors = []
        for contributor in obj.contributors.all():
            contributors.append({'id': contributor.user.id,
                                 'username': contributor.user.username,
                                 'role': contributor.role})
        return contributors

    def get_issues(self, obj):
        issues = []
        for issue in obj.issue_set.all():
            issues.append({'id': issue.id,
                           'title': issue.title})
        return issues


# Contributor Serializers
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


# Issue Serializers
class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag', 'priority', 'status']


class IssueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'project', 'status', 'author', 'assignee', 'created_time']
        read_only_fields = ['project', 'created_time', 'author']


class IssueDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    assignee = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'project', 'status', 'author', 'assignee', 'created_time', 'comments']
        read_only_fields = ['project', 'created_time', 'author']

    def get_author(self, obj):
        return {'id': obj.author.id,
                'username': obj.author.username}

    def get_assignee(self, obj):
        return {'id': obj.assignee.id,
                'username': obj.assignee.username}

    def get_comments(self, obj):
        comments = []
        for comment in obj.comment_set.all():
            comments.append({'id': comment.id,
                             'description': comment.description})
        return comments


# Comment Serializers
class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author']

    def get_author(self, obj):
        return obj.author.username


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
        read_only_fields = ['issue', 'created_time', 'author']


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    issue = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
        read_only_fields = ['issue', 'created_time', 'author']

    def get_author(self, obj):
        return {'id': obj.author.id,
                'username': obj.author.username}

    def get_issue(self, obj):
        return {'id': obj.issue.id,
                'title': obj.issue.title}
