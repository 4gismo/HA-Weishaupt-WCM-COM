"""Switch to pause/resume WCM-COM polling."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WeishauptBaseEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    async_add_entities([WeishauptPauseSwitch(hass)])


class WeishauptPauseSwitch(WeishauptBaseEntity, SwitchEntity):

    _attr_has_entity_name = True
    _attr_translation_key = "polling"

    def __init__(self, hass):
        super().__init__(hass)
        self._attr_unique_id = "weishaupt_wcm_polling"

    @property
    def is_on(self):
        return not self.api()._paused

    @property
    def icon(self):
        return "mdi:play-circle" if self.is_on else "mdi:pause-circle"

    async def async_turn_on(self, **kwargs):
        self.api().resume()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self.api().pause()
        self.async_write_ha_state()
