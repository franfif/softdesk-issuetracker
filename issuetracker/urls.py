
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from issues.views import ProjectViewSet

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
