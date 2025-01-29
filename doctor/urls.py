"""
URL configuration for doctor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# DRF YASG
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# def trigger_error(request):
#     division_by_zero = 1 / 0


schema_view = get_schema_view(
    openapi.Info(
        title="United Accreditation Foundation",
        default_version="v1",
        description="REST implementation of Django authentication system. "
                    "djoser library provides a set of Django "
                    "Rest Framework views to handle basic actions such as "
                    "registration, login, logout, password reset "
                    "and account activation. It works with custom user model.",
        contact=openapi.Contact(email="nandk@thinkdatalabs.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'swagger/^$', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^$', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
    re_path(
        r"^testing/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path("sentry-debug/", trigger_error),
    path('api/account/', include('account.urls')),
    path('api/management/', include('management.urls')),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
