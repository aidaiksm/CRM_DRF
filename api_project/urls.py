"""api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from flights.views import FlightViewSet
from reports.views import ReportViewSet, CommentViewSet, StatusReportView

router = DefaultRouter()
router.register('flights', FlightViewSet)
router.register('reports', ReportViewSet)
router.register(r'comments', CommentViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="CRM API",
        default_version='v1',
        description="Welcome! Everything is fine.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('admin/reports/', include('reports.urls', 'reports')),
    path('api/v1/accounts/', include('users.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/reports/<int:pk>/status/', StatusReportView.as_view()),

]

if settings.DEBUG is True:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
