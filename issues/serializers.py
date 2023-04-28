from django.contrib.auth import get_user_model

from .models import Project, Contributor, Issue, Comment
from rest_framework import serializers


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user']


class ProjectSerializer(serializers.ModelSerializer):
    # contributors = serializers.SerializerMethodField()
    contributors = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'owner', 'contributors']
        # fields = ['id', 'title', 'description', 'type', 'owner']

    # def get_contributors(self, instance):
    #     queryset = instance.contributors.all()
    #     serializer = ContributorSerializer(queryset, many=True)
    #     return serializer.data

    def create(self, validated_data):
        # get request in the serializer from context
        print('Project create - validated_data')
        print(validated_data)
        contributors_data = validated_data.pop('contributors')
        # project = super().create(validated_data)
        project = Project.objects.create(**validated_data)

        request = self.context.get('request')
        owner = request.user
        project.contributors.add(Contributor.objects.create(user=owner,
                                                            role=Contributor.OWNER,
                                                            project=project))
        # contributor_ids = []
        for contributor_data in contributors_data:
            print('Project create - contributor_data')
            print(contributor_data)
            Contributor.objects.create(project=project, role=Contributor.CONTRIBUTOR, **contributor_data)

        # project.contributors.set(contributor_ids)
        return project

    def update(self, instance, validated_data):
        print('Project update - validated_data')
        print(validated_data)
        print('instance')
        print(instance)
        contributors_data = validated_data.pop('contributors')
        project = Project.objects.update(instance, **validated_data)
        for contributor_data in contributors_data:
            print(contributor_data)
            Contributor.objects.create(project=project,
                                       role=Contributor.CONTRIBUTOR,
                                       **contributor_data)
        return project

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
