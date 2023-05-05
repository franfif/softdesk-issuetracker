
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from issues import views

# router = routers.SimpleRouter()
# router.register(r'projects', ProjectViewSet, basename='project')
# router.register(r'projects/<int:pk>/users', ProjectContributorViewSet, basename='project-user')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('', include(router.urls)),

    path('token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('projects/',
         views.ProjectListAPIView.as_view(),
         name='project-list'),
    path('projects/<int:pk>/',
         views.ProjectDetailAPIView.as_view(),
         name='project-detail'),
    path('projects/<int:project_id>/users/',
         views.ContributorListAPIView.as_view(),
         name='contributor-list'),
    path('projects/<int:project_id>/users/<int:id>/',
         views.ContributorDestroyAPIView.as_view(),
         name='contributor-detail'),
    path('projects/<int:project_id>/issues/',
         views.IssueListAPIView.as_view(),
         name='issue-list'),
    path('projects/<int:project_id>/issues/<int:id>/',
         views.IssueDetailAPIView.as_view(),
         name='issue-detail'),
    path('projects/<int:project_id>/issues/<issue_id>/comments/',
         views.CommentListAPIView.as_view(),
         name='comment-list'),
    path('projects/<int:project_id>/issues/<issue_id>/comments/<int:id>/',
         views.CommentDetailAPIView.as_view(),
         name='comment-detail'),
    # path('contributors/',
    #      views.ContributorListAPIView.as_view(),
    #      name='contributor-list'),
]
