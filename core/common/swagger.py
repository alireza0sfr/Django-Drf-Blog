from rest_framework.permissions import IsAdminUser
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

DEFAULT_VERSION = 'v1.0'

schema_view = get_schema_view(
   openapi.Info(
      title="Todo Api's",
      default_version= DEFAULT_VERSION,
      description="simple todo app",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="alireza.safaree@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[IsAdminUser],
)