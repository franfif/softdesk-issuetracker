
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

import authentication.views
from issues import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('signup/',
         authentication.views.UserCreate.as_view(),
         name="signup"),
    path('login/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    # refresh token: if needed, uncomment these lines.
    # path('login/refresh/',
    #      TokenRefreshView.as_view(),
    #      name='token_refresh'),

    path('projects/',
         views.ProjectListAPIView.as_view(),
         name='project-list'),
    path('projects/<int:id>/',
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
]
