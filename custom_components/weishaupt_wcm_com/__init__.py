"""Weishaupt WCM-COM Integration."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.discovery import async_load_platform

from .const import DOMAIN
from .api import WeishauptAPI

from homeassistant.const import (
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """YAML-based setup."""
    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]
    api = WeishauptAPI(conf[CONF_HOST], conf[CONF_USERNAME], conf[CONF_PASSWORD])
    hass.data[DOMAIN] = api

    await async_load_platform(hass, "sensor", DOMAIN, {}, config)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """UI-based setup via config entry."""
    api = WeishauptAPI(entry.data[CONF_HOST], entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
    hass.data[DOMAIN] = api

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "binary_sensor", "select", "switch"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_sensor = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    unload_binary = await hass.config_entries.async_forward_entry_unload(entry, "binary_sensor")
    unload_select = await hass.config_entries.async_forward_entry_unload(entry, "select")
    unload_switch = await hass.config_entries.async_forward_entry_unload(entry, "switch")
    hass.data.pop(DOMAIN, None)
    return unload_sensor and unload_binary and unload_select and unload_switch

class WeishauptBaseEntity:
    def __init__(self, hass, config=None):
        self._api = hass.data[DOMAIN]

    def api(self):
        return self._api

    def update(self):
        _LOGGER.debug("API Update")
        self._api.update()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "weishaupt_wcm")},
            "name": "Weishaupt WCM-COM",
            "manufacturer": "Weishaupt",
            "model": "WCM-COM",
            "configuration_url": f"http://{self._api._host}/",
        }
