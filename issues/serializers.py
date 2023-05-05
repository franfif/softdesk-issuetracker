from .models import Project, Contributor, Issue, Comment
from rest_framework import serializers


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'role', 'project']
        read_only_fields = ['role', 'project']


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'owner', 'contributors']
        read_only_fields = ['owner']

    def get_owner(self, obj):
        return obj.owner.username

    def get_contributors(self, obj):
        names = []
        for contributor in obj.contributors.all():
            names.append(contributor.user.username)
        return names

    def create(self, validated_data):
        # get request in the serializer from context
        request = self.context.get('request')
        owner = request.user

        project = Project.objects.create(owner=owner, **validated_data)

        project.contributors.add(Contributor.objects.create(user=owner,
                                                            role=Contributor.OWNER,
                                                            project=project))
        return project


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'project', 'status', 'author', 'assignee', 'created_time']
        read_only_fields = ['project', 'created_time', 'author']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'project', 'issue', 'created_time']
        read_only_fields = ['project', 'issue', 'created_time', 'author']
