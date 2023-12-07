from django.urls import path, include
from openai_app import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# noinspection PyTypeChecker
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('index/', views.index),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('pdf/', views.OpenApITextExtractionAPI.as_view())
]