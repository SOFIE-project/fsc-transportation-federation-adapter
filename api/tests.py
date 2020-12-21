from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from api.indy import IndyClient
from api.views import RetrieveTransportsView

transports = [
    '0xf9535bac1c0dacfe011b6a07ce55ad3fdc761de7345d7b004778e93b9d222ae5'
]


class MockTransportationClient:
    @property
    def transport_ids(self):
        return transports


class TransportationAdapterTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def tearDown(self) -> None:
        super().tearDown()

    def test_things_description_page(self):
        url = reverse('things_description')
        res = self.client.get(url)
        td = res.json()
        self.assertEquals(td['title'], 'TransportationThing', 'Transportation Things Description Model retrieved')

    def test_federation_adapter_did_retrieval(self):
        url = reverse('things_description')
        res = self.client.get(url)
        self.assertEquals(res['indy-did'], IndyClient().did[0], 'Federation Adapter did retrieved')

    def test_retrieve_transports(self):
        url = reverse('retrieve_transports')
        with patch.object(RetrieveTransportsView, 'transportation_client', MockTransportationClient()):
            res = self.client.get(url)
        data = res.json()
        self.assertEquals(data['transports'], transports)
