import logging
import pickle
from collections import defaultdict
from datetime import timedelta

import redis
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from pymongo import MongoClient
from web3 import Web3

log = logging.getLogger(__name__)


class TransportationClient:
    REDIS_KEY = '_TRANSPORTS'
    REDIS_KEY_TTL = 5  # in seconds
    DAYS_PAST = 1  # how far in the past to look for `active` transports

    def __init__(self):
        # Initialize mongodb client
        if not settings.MONGODB_USER:
            host = 'mongodb://{}:{}/{}'.format(
                settings.MONGODB_HOST,
                settings.MONGODB_PORT,
                settings.MONGODB_DATABASE
            )
        else:
            host = 'mongodb://{}:{}@{}:{}/{}'.format(
                settings.MONGODB_USER,
                settings.MONGODB_PASSWORD,
                settings.MONGODB_HOST,
                settings.MONGODB_PORT,
                settings.MONGODB_DATABASE
            )

        self.client = MongoClient(host=host)
        self.db = self.client[settings.MONGODB_DATABASE]
        self.collection = self.db[settings.MONGODB_COLLECTION]

        # Initialize redis client
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE
        )

        self.transports = defaultdict()

        # Get cached transports
        transports_picked = self.redis.get(self.REDIS_KEY)

        # If cache miss, fetch new data from KAA
        if not transports_picked:
            log.info('Cache miss. Fetching from KAA...')
            self.initialize()
        else:
            log.info('Cache hit, loading from redis...')
            self.transports = pickle.loads(transports_picked)

    @cached_property
    def transport_ids(self):
        return self.transports.keys()

    def initialize(self):
        for transport in self.retrieve_transports():
            key = int('0x' + transport, 16)  # convert hexstring gateway id to integer
            key = Web3.sha3(text=str(key))   # stringified integer form is passed to sha3
            key = key.hex()                  # convert to hexstring

            self.transports[key] = transport

        self.redis.set(self.REDIS_KEY, pickle.dumps(self.transports), self.REDIS_KEY_TTL)

    def retrieve_transports(self, now=None):
        """Retrieves the `active` transports.
        Active transport is defined as the transport that has send a measurements in the past `self.DAYS_PAST` days

        Args:
            now (datetime): the present measurement (optional) defaults to now

        Returns:
            list - the list of gatewayIds as returned from KAA
        """
        if not now:
            now = timezone.now()

        now_millis = int(round(now.timestamp() * 1000))

        res = self.collection.find({
            'header.timestamp.long': {
                '$gte': now_millis - self.DAYS_PAST * 60 * 60 * 24 * 1000
            }}).distinct('event.GatewayId')

        return [transport for transport in res]

    def retrieve_boxes(self, transport_id, now=None, seconds_before=1*60):
        """Retrieves the boxes inside the given transport for the given moment.

        Args:
            transport_id (str): the hashed transport id
            now (datetime): when to consider the present moment
            seconds_before (int): how far in the past to look for KAA measurements (depends on rPI data rate)

        Returns:
            list - the list of present boxes in the given transport
        """
        if not now:
            now = timezone.now()

        start = int(round((now - timedelta(seconds=seconds_before)).timestamp() * 1000))
        end = int(round(now.timestamp() * 1000))

        pipeline = [
            {
                '$match': {
                    '$and': [
                        {'event.GatewayId': self.transports[transport_id]},
                        {'header.timestamp.long': {'$gte': start, '$lte': end}}
                    ]
                }
            },
            {
                '$group': {
                    '_id': None,
                    'gateway_id': {'$first': '$event.GatewayId'},
                    'boxes': {'$first': '$event.BoxIdsPresent'},
                    'timestamp': {'$max': '$header.timestamp.long'}
                }
            }
        ]

        res = self.collection.aggregate(pipeline)

        boxes = []
        docs = [doc for doc in res]

        # Either one document returned or zero
        try:
            boxes = docs[0]['boxes']
        except IndexError:
            pass

        return boxes

    def retrieve_transport_readings(self, transport_id, start, end=None):
        """Returns the aggregated min,max,avg sensor measurements for the given transport for the given timeframe.

        Args:
            transport_id (str): the hashed transport id
            start (datetime): the datetime object to start measurements from
            end (datetime): the datetime object to end measurements, optional, defaults to now

        Returns:
            dict - the aggregated sensor readings or None if no sensor data found, e.g.:
                {'avg_temperature': 26.033746776894656, 'min_temperature': 19.9, 'max_temperature': 29.33}
        """

        if not end:
            end = timezone.now()

        end = int(round(end.timestamp() * 1000))
        start = int(round(start.timestamp() * 1000))

        pipeline = [
            {
                '$match': {
                    '$and': [
                        {'event.GatewayId': self.transports[transport_id]},
                        {'header.timestamp.long': {'$gte': start, '$lte': end}}
                    ]
                }
            },
            {
                '$group': {
                    '_id': None,
                    'avg_temperature': {'$avg': '$event.Temperature'},
                    'min_temperature': {'$min': '$event.Temperature'},
                    'max_temperature': {'$max': '$event.Temperature'}
                }
            },
            {
                '$project': {'_id': 0}
            }
        ]

        res = self.collection.aggregate(pipeline)
        docs = [doc for doc in res]
        readings = None

        # Either one or none documents returned
        try:
            readings = docs[0]
        except IndexError:
            pass

        return readings
