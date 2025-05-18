import json
import logging
from datetime import timedelta
from homeassistant.util import Throttle
from weishaupt_wcm_com import heat_exchanger

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

class WeishauptAPI:
    def __init__(self, host, username, password):
        self._host = host
        self._username = username
        self._password = password
        self._data = {}

    def getData(self):
        return self._data

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        result = heat_exchanger.process_values(self._host, self._username, self._password)
        _LOGGER.debug("Fetching new data")
        if result is not None:
            self._data = json.loads(result)
        else:
            _LOGGER.warning("Cannot update data from WCM-COM")
