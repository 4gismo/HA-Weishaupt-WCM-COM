"""Platform for sensor integration."""
from homeassistant.const import UnitOfTemperature
from homeassistant.components.sensor import SensorEntity
import logging
from datetime import timedelta, datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .const import NAME_PREFIX

from .const import OIL_CONSUMPTION_KEY
from .const import OUTSIDE_TEMPERATURE_KEY
from .const import LOAD_SETTING_KEY
from .const import WARM_WATER_TEMPERATURE_KEY 
from .const import FLOW_TEMPERATURE_KEY
from .const import FLUE_GAS_TEMPERATURE_KEY
from .const import MIXED_EXTERNAL_TEMPERATURE_KEY
from .const import ROOM_TEMPERATURE_KEY
from .const import OPERATING_MODE_KEY
from .const import OPERATING_PHASE_KEY
from .const import PUMP_KEY
from .const import WARM_WATER_KEY
from .const import FLAME_KEY
from .const import ERROR_KEY
from .const import GAS_VALVE_1_KEY
from .const import GAS_VALVE_2_KEY
from .const import HEATING_KEY

from . import WeishauptBaseEntity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    if discovery_info is None:
        return
    add_entities(_build_entities(hass, config))

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the sensor platform via config entry (UI)."""
    async_add_entities(_build_entities(hass, {}))

def _build_entities(hass, config):
    return [
        WeishauptSensor(hass, config, OIL_CONSUMPTION_KEY, "l"),
        WeishauptSensor(hass, config, OUTSIDE_TEMPERATURE_KEY, "°C"),
        WeishauptSensor(hass, config, LOAD_SETTING_KEY, "kW"),
        WeishauptSensor(hass, config, WARM_WATER_TEMPERATURE_KEY, "°C"),
        WeishauptSensor(hass, config, FLOW_TEMPERATURE_KEY, "°C"),
        WeishauptSensor(hass, config, FLUE_GAS_TEMPERATURE_KEY, "°C"),
        WeishauptSensor(hass, config, ROOM_TEMPERATURE_KEY, "°C"),
        WeishauptSensor(hass, config, MIXED_EXTERNAL_TEMPERATURE_KEY, "°C"),
        WeishauptSensor(hass, config, OPERATING_MODE_KEY, ""),
        WeishauptSensor(hass, config, OPERATING_PHASE_KEY, ""),
        WeishauptSensor(hass, config, PUMP_KEY, ""),
        WeishauptSensor(hass, config, WARM_WATER_KEY, ""),
        WeishauptSensor(hass, config, FLAME_KEY, ""),
        WeishauptSensor(hass, config, ERROR_KEY, ""),
        WeishauptSensor(hass, config, GAS_VALVE_1_KEY, ""),
        WeishauptSensor(hass, config, GAS_VALVE_2_KEY, ""),
        WeishauptSensor(hass, config, HEATING_KEY, ""),
    ]

class WeishauptSensor(WeishauptBaseEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass, config, sensor_name, sensor_unit):
        super().__init__(hass, config)
        """Initialize the sensor."""
        self._state = None
        self._data = {}
        self._config = config
        self._name = sensor_name
        self._unit = sensor_unit

    @property
    def name(self):
        """Return the name of the sensor."""
        return NAME_PREFIX + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    async def async_update(self):
        _LOGGER.debug(f"[async_update] Updating sensor: {self._name}")
        await self.hass.async_add_executor_job(super().update)
        try:
            self._state = self.api().getData().get(self._name)
        except Exception as e:
            _LOGGER.warning(f"[async_update] Failed to update sensor {self._name}: {e}")
            self._state = None
