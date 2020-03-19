import json

from django.conf import settings


class ThingDescriptionParser:
    """Parses the thing description json file and performs any necessary post processing
    """
    def __init__(self, *args, **kwargs):
        with open(settings.THING_DESCRIPTION_PATH) as json_file:
            td_string = json_file.read().replace('{BASE}', settings.EXTERNAL_BASE_URI)

        self.td = json.loads(td_string)




