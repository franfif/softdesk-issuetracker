from django.contrib.auth import get_user_model

from .models import Project, Contributor, Issue, Comment
from rest_framework import serializers


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user', 'role']


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors']

    # def create(self, validated_data):
    #     owner = get_user_model()
    #     return Project.objects.create(**validated_data)


class ProjectContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectContributor
        fields = ['id', 'project', 'contributor', 'role']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'project', 'status', 'author', 'assignee', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue', 'created_time']
