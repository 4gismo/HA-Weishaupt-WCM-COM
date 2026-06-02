"""Platform for select integration."""
import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import OPERATING_MODE_KEY
from . import WeishauptBaseEntity

_LOGGER = logging.getLogger(__name__)

# Maps HA option key → device value (from device XML idT0112HK)
OPERATING_MODE_OPTIONS: dict[str, int] = {
    "standby": 1,
    "normal": 3,
    "setback": 4,
    "summer": 5,
    "program_1": 11,
    "program_2": 12,
    "program_3": 13,
    "follow_master": 255,
}

_VALUE_TO_OPTION: dict[int, str] = {v: k for k, v in OPERATING_MODE_OPTIONS.items()}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    async_add_entities([WeishauptOperatingModeSelect(hass, {})])


class WeishauptOperatingModeSelect(WeishauptBaseEntity, SelectEntity, RestoreEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "operating_mode_hk"
    _attr_unique_id = "weishaupt_wcm_operating_mode"
    _attr_options = list(OPERATING_MODE_OPTIONS.keys())

    def __init__(self, hass, config):
        super().__init__(hass, config)
        self._restored_option: str | None = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state in self._attr_options:
            self._restored_option = last_state.state
            _LOGGER.debug("Restored operating mode: %s", self._restored_option)

    @property
    def current_option(self) -> str | None:
        value = self.api().getData().get(OPERATING_MODE_KEY)
        if value is not None:
            option = _VALUE_TO_OPTION.get(int(value))
            if option is None:
                _LOGGER.warning("Operating Mode value %s from device is not in known options %s", value, list(_VALUE_TO_OPTION.keys()))
            return option
        return self._restored_option

    async def async_select_option(self, option: str) -> None:
        mode_value = OPERATING_MODE_OPTIONS[option]
        _LOGGER.info("Setting Operating Mode HK to %s (%d)", option, mode_value)
        await self.hass.async_add_executor_job(self.api().set_operating_mode, mode_value)
        self.async_write_ha_state()

    async def async_update(self):
        _LOGGER.debug("[async_update] Updating operating mode select")
        await self.hass.async_add_executor_job(super().update)
