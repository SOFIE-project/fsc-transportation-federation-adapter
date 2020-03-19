from rest_framework import serializers


class RetrieveTransportsSerializer(serializers.Serializer):
    transports = serializers.ListField(
        help_text='The list of transport ids',
        child=serializers.CharField(max_length=66, min_length=66, help_text='The hashed/encrypted id of the transport')
    )


class RetrieveTransportBoxesSerializer(serializers.Serializer):
    transport_boxes = serializers.ListField(
        help_text='The list of box ids',
        child=serializers.CharField(max_length=10, min_length=10, help_text='The id of the box')
    )


class RetrieveTransportReadingsFieldsSerializer(serializers.Serializer):
    min_temperature = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    max_temperature = serializers.FloatField()


class RetrieveTransportReadingsSerializer(serializers.Serializer):
    transport_readings = RetrieveTransportReadingsFieldsSerializer()
