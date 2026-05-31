import json
import logging
from datetime import timedelta
from homeassistant.util import Throttle
from weishaupt_wcm_com import heat_exchanger
import requests

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
        _LOGGER.debug("Connecting to WCM-COM at %s with user %s", self._host, self._username)
        try:
            result = heat_exchanger.process_values(self._host, self._username, self._password)
            self._data = json.loads(result)
            _LOGGER.debug("Received data: %s", json.dumps(self._data, indent=2))
        except requests.exceptions.ConnectionError:
            _LOGGER.error("WCM-COM not reachable at http://%s — check host/IP", self._host)
        except requests.exceptions.Timeout:
            _LOGGER.error("WCM-COM at %s did not respond within 5s", self._host)
        except requests.exceptions.HTTPError as e:
            _LOGGER.error("WCM-COM auth or HTTP error at %s: %s", self._host, e)
        except requests.exceptions.RequestException as e:
            _LOGGER.error("WCM-COM request failed: %s", e)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            _LOGGER.error("WCM-COM returned unexpected response format: %s", e)
        except Exception as e:
            _LOGGER.error("WCM-COM unexpected error: %s", e)
