
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from issues import views

# router = routers.SimpleRouter()
# router.register(r'projects', ProjectViewSet, basename='project')
# router.register(r'projects/<int:pk>/users', ProjectContributorViewSet, basename='project-user')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('', include(router.urls)),
    path('projects/',
         views.ProjectListAPIView.as_view(),
         name='project-list'),
    path('projects/<int:pk>/',
         views.ProjectDetailAPIView.as_view(),
         name='project-detail'),
    path('projects/<int:project_pk>/users/',
         views.ContributorListAPIView.as_view(),
         name='contributor-list'),
    # path('projects/<int:project_pk>/users/<int:user_pk>/',
    #      views.ContributorDetailAPIView.as_view(),
    #      name='contributor-detail'),
    path('projects/<int:project_pk>/issues/',
         views.IssueListAPIView.as_view(),
         name='issue-list'),
    path('projects/<int:project_pk>/issues/<issue_pk>/',
         views.IssueDetailAPIView.as_view(),
         name='issue-detail'),
    path('projects/<int:project_pk>/issues/<issue_pk>/comments/',
         views.CommentListAPIView.as_view(),
         name='comment-list'),
    path('projects/<int:project_pk>/issues/<issue_pk>/comments/<int:comment_pk>/',
         views.CommentDetailAPIView.as_view(),
         name='comment-detail'),
    # path('contributors/',
    #      views.ContributorListAPIView.as_view(),
    #      name='contributor-list'),
]
