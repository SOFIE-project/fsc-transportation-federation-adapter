from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

from api.td import ThingDescriptionParser


def things_description_view(request, *args, **kwargs):
    """Returns the things description in json format
    """
    parser = ThingDescriptionParser()
    return JsonResponse(parser.td)


urlpatterns = [
    path('', things_description_view),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.PROXY_PREFIX:
    urlpatterns = [path(settings.PROXY_PREFIX + '/', include(urlpatterns))]
