from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings


# Swagger Schema View with JWT Support
schema_view = get_schema_view(
    openapi.Info(
        title="EduConnect API",
        default_version='v1',
        description="API for Student-Teacher Assignment Portal",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Inject JWT Bearer support into Swagger
swagger_settings.SECURITY_DEFINITIONS = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter JWT token as: Bearer <your_token>'
    }
}


# Optional root health check view
def root_view(request):
    return JsonResponse({"message": "Welcome to EduConnect API!"})

urlpatterns = [
    path('', root_view),
    path("admin/", admin.site.urls),

    # JWT Auth
    path('api/login/token', TokenObtainPairView.as_view(), name='unified_login'),
    path('api/login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Modular API includes
    path('api/users/', include('apps.users.urls')),
    path('api/assignments/', include('apps.assignments.urls')),

    # Swagger/OpenAPI Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve uploaded files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
