from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

from api.indy import IndyClient
from api.td import ThingDescriptionParser


def things_description_view(request, *args):
    """Returns the things description in json format
    """
    parser = ThingDescriptionParser()
    response = JsonResponse(parser.td)

    # Attach Indy headers
    indy_client = IndyClient()
    did, verkey = indy_client.did
    response['Indy-Did'] = did
    response['Indy-Verkey'] = verkey

    return response


urlpatterns = [
    path('', things_description_view, name='things_description'),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.PROXY_PREFIX:
    urlpatterns = [path(settings.PROXY_PREFIX + '/', include(urlpatterns))]
