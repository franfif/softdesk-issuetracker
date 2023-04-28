from django.contrib.auth import get_user_model

from .models import Project, Contributor, Issue, Comment
from rest_framework import serializers


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    # contributors = ContributorSerializer(many=True)
    # cont = serializers.SerializerMethodField()

    class Meta:
        model = Project
        # fields = ['id', 'title', 'description', 'type', 'owner', 'contributors']
        fields = ['id', 'title', 'description', 'type', 'owner']

    # def get_cont(self, instance):
    #     queryset = instance,

    # def create(self, validated_data):
    #     contributors = validated_data.pop('contributors')
    #     project = Project.objects.create(**validated_data)
    #     contributor_ids = []
    #     for contributor in contributors:
    #         contributor_ids.append(contributor.id)
    #
    #     project.contributors.set(contributor_ids)
    #     return project
    #
    # def update(self, instance, validated_data):
    #     contributors = validated_data.pop('contributors')
    #     project = super().update(instance, **validated_data)
    #     for contributor in contributors:
    #         project.contributors.add(contributor.contributor,
    #                                  through_default={'role': 'Contributor'})
    #     return project

    # def create(self, validated_data):
    #     # get request in the serializer from context
    #     request = self.context.get('request')
    #     owner = request.user
    #     project = super().create(validated_data)
    #     project.contributors.add(owner,
    #                              through_defaults={'role': 'Owner'})
    #     return project


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'project', 'status', 'author', 'assignee', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue', 'created_time']
