from django.conf.urls import url
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

API_DESCRIPTION = """Api endpoints exposed by the SOFIE Food Supply Chain Transportation Federation Adapter.

The `swagger-ui` view can be found [here](/api/swagger).  
The `ReDoc` view can be found [here](/api/redoc).  
The swagger YAML document can be found [here](/api/swagger.yaml).  
"""

schema_view = get_schema_view(
   openapi.Info(
      title="SOFIE Food Supply Chain Transportation Federation Adapter API",
      default_version='v1',
      description=API_DESCRIPTION,
   ),
   validators=[],
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('transports', views.RetrieveTransportsView.as_view(), name='retrieve_transports'),
    path('transport/<str:transport_id>/boxes', views.RetrieveTransportBoxesView.as_view(), name='retrieve_transport_boxes'),
    path('transport/<str:transport_id>/readings', views.RetrieveTransportReadingsView.as_view(), name='retrieve_transport_readings')
]
