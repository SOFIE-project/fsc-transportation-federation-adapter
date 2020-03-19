from dateutil.parser import parse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from api.serializers import RetrieveTransportsSerializer, RetrieveTransportBoxesSerializer, \
    RetrieveTransportReadingsSerializer
from api.transportation import TransportationClient

START_PARAMETER = openapi.Parameter(
    'start', openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description='The start time of the measurement',
    required=True
)

END_PARAMETER = openapi.Parameter(
    'end', openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description='The end time of the measurement',
    required=False
)


class TransportationClientProviderMixin:
    """Provides an instance to a Transport client
    """

    @property
    def transportation_client(self):
        return TransportationClient()


class RetrieveTransportsView(RetrieveAPIView, TransportationClientProviderMixin):
    """Retrieves the transport ids.
    """
    serializer_class = RetrieveTransportsSerializer

    def get_object(self):
        transport_ids = self.transportation_client.transport_ids
        return {'transports': transport_ids}


class RetrieveTransportBoxesView(RetrieveAPIView, TransportationClientProviderMixin):
    """Retrieve the boxes of a given transport.
    """

    serializer_class = RetrieveTransportBoxesSerializer
    lookup_url_kwarg = 'transport_id'

    def get(self, request, *args, **kwargs):
        self.transport_id = kwargs.get(self.lookup_url_kwarg)
        self.client = self.transportation_client
        if self.transport_id not in self.client.transport_ids:
            return Response({'reason': 'Invalid transport'}, status=status.HTTP_400_BAD_REQUEST)

        return super(RetrieveTransportBoxesView, self).get(request, *args, **kwargs)

    def get_object(self):
        boxes = self.transportation_client.retrieve_boxes(self.transport_id)
        return {'transport_boxes': boxes}


class RetrieveTransportReadingsView(RetrieveAPIView, TransportationClientProviderMixin):
    """Retrieves the sensor readings of a given transport
    """
    serializer_class = RetrieveTransportReadingsSerializer
    lookup_url_kwarg = 'transport_id'

    @swagger_auto_schema(manual_parameters=[START_PARAMETER, END_PARAMETER])
    def get(self, request, *args, **kwargs):
        self.start = self.request.GET.get('start')

        try:
            self.start = parse(self.start)
        except Exception as e:
            return Response({'reason': 'Invalid start date'}, status=status.HTTP_400_BAD_REQUEST)

        self.end = self.request.GET.get('end', None)
        if self.end:
            try:
                self.end = parse(self.end)
            except Exception as e:
                return Response({'reason': 'Invalid end date'}, status=status.HTTP_400_BAD_REQUEST)

        self.transport_id = kwargs.get(self.lookup_url_kwarg)
        self.client = self.transportation_client
        if self.transport_id not in self.client.transport_ids:
            return Response({'reason': 'Invalid transport'}, status=status.HTTP_400_BAD_REQUEST)

        return super(RetrieveTransportReadingsView, self).get(request, *args, **kwargs)

    def get_object(self):
        readings = self.transportation_client.retrieve_transport_readings(self.transport_id, self.start, self.end)
        return {'transport_readings': readings}
