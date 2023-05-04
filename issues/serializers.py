from .models import Project, Contributor, Issue, Comment
from rest_framework import serializers


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'role', 'project']
        read_only_fields = ['role', 'project']


class ProjectSerializer(serializers.ModelSerializer):
    # contributors = serializers.SerializerMethodField()
    # contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        # fields = ['id', 'title', 'description', 'type', 'owner', 'contributors']
        fields = ['id', 'title', 'description', 'type', 'owner']
        read_only_fields = ['owner']

    # def get_contributors(self, instance):
    #     queryset = instance.contributors.all()
    #     serializer = ContributorSerializer(queryset, many=True)
    #     return serializer.data

    def create(self, validated_data):
        # contributors_data = validated_data.pop('contributors')

        # get request in the serializer from context
        request = self.context.get('request')
        owner = request.user

        # project = super().create(validated_data)
        project = Project.objects.create(owner=owner, **validated_data)

        project.contributors.add(Contributor.objects.create(user=owner,
                                                            role=Contributor.OWNER,
                                                            project=project))
        # for contributor_data in contributors_data:
        #     if contributor_data['user'] != owner:
        #         Contributor.objects.create(project=project,
        #                                    role=Contributor.CONTRIBUTOR,
        #                                    **contributor_data)

        return project

    def update(self, instance, validated_data):
        # contributors_data = validated_data.pop('contributors')
        project = super().update(instance, validated_data)

        # # Convert contributors_data to a list of users
        # new_contributors = list(map(lambda c: c['user'], contributors_data))
        # # Convert the existing contributors of this project to a list of users
        # existing_contributors = list(map(lambda c: c.user, Contributor.objects.filter(project=project)))
        #
        # # Create new contributors if the user is not already a contributor
        # for user in (user for user in new_contributors if user not in existing_contributors):
        #     Contributor.objects.create(project=project,
        #                                role=Contributor.CONTRIBUTOR,
        #                                user=user)
        # # Remove contributors who are not in the updated data
        # for user in (user for user in existing_contributors if user not in new_contributors):
        #     # TO DO? Do we want to prevent the suppression of the contributor if they are the project's owner?
        #     Contributor.objects.get(project=project, user=user).delete()

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
        read_only_fields = ['project', 'created_time', 'author']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue', 'created_time']
