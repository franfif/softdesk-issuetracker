from rest_framework import permissions

from .models import Contributor


class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_owner = Contributor.objects.filter(project=obj,
                                              user=request.user,
                                              role=Contributor.OWNER).exists()
        return obj.owner == request.user or is_owner


class IsProjectContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        project = view.kwargs.get('project_id')
        is_contributor = Contributor.objects.filter(project=project,
                                                    user=request.user).exists()
        return is_contributor


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
