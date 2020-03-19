from datetime import datetime, timedelta

from django.core.management import BaseCommand

from api.aberon import AberonClient
from api.transportation import TransportationClient


class Command(BaseCommand):
    """Use only for development!
    """

    def handle(self, *args, **options):
        client = TransportationClient()
        dt_object = datetime.fromtimestamp(1568111312)
        # r = client.retrieve_boxes('0x46ff9921da43e9b388eaa5fc7b1166abc9965641a82d188da2cdf782ef6058e6', now=dt_object)
        # print(r)


        start = dt_object - timedelta(days=180)

        r = client.retrieve_transport_readings(
            '0x46ff9921da43e9b388eaa5fc7b1166abc9965641a82d188da2cdf782ef6058e6',
            start

        )

        print(r)
