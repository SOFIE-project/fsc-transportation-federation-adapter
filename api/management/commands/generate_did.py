import asyncio

from django.core.management import BaseCommand

from api.indy import IndyClient


class Command(BaseCommand):
    help = 'Gets or creates the DID of the Federation Adapter'

    def handle(self, *args, **options):
        self.stdout.write("Getting or creating client Indy wallet and DID...")
        indy_client = IndyClient()
        did, verkey = indy_client.did
        self.stdout.write(self.style.SUCCESS("DID: " + did))
        self.stdout.write(self.style.SUCCESS("Verification key: " + verkey))
