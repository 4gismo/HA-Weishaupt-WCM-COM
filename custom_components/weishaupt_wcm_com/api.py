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
        _LOGGER.debug(f"Connecting to WCM-COM at {self._host} with user {self._username}")
        try:
            result = heat_exchanger.process_values(self._host, self._username, self._password)
            if result:
                self._data = json.loads(result)
                _LOGGER.debug(f"Received data: {json.dumps(self._data, indent=2)}")
            else:
                _LOGGER.warning("WCM-COM returned no data � possible auth or network issue.")
        except Exception as e:
            _LOGGER.error(f"Exception during WCM-COM update: {e}")
