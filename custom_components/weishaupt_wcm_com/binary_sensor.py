"""Platform for binary sensor integration."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    PUMP_KEY,
    WARM_WATER_KEY,
    FLAME_KEY,
    GAS_VALVE_1_KEY,
    GAS_VALVE_2_KEY,
    HEATING_KEY,
)
from . import WeishauptBaseEntity

_LOGGER = logging.getLogger(__name__)

BINARY_SENSOR_DESCRIPTIONS: dict[str, BinarySensorEntityDescription] = {
    FLAME_KEY: BinarySensorEntityDescription(
        key=FLAME_KEY,
        translation_key="flame",
        device_class=BinarySensorDeviceClass.HEAT,
    ),
    GAS_VALVE_1_KEY: BinarySensorEntityDescription(
        key=GAS_VALVE_1_KEY,
        translation_key="gas_valve_1",
        device_class=BinarySensorDeviceClass.OPENING,
    ),
    GAS_VALVE_2_KEY: BinarySensorEntityDescription(
        key=GAS_VALVE_2_KEY,
        translation_key="gas_valve_2",
        device_class=BinarySensorDeviceClass.OPENING,
    ),
    HEATING_KEY: BinarySensorEntityDescription(
        key=HEATING_KEY,
        translation_key="heating",
        device_class=BinarySensorDeviceClass.HEAT,
    ),
    WARM_WATER_KEY: BinarySensorEntityDescription(
        key=WARM_WATER_KEY,
        translation_key="warm_water",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    PUMP_KEY: BinarySensorEntityDescription(
        key=PUMP_KEY,
        translation_key="pump",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
}

# State-dependent icons per entity key: (icon_on, icon_off)
_ICONS: dict[str, tuple[str, str]] = {
    FLAME_KEY:      ("mdi:fire",          "mdi:fire-off"),
    PUMP_KEY:       ("mdi:pump",           "mdi:pump-off"),
    HEATING_KEY:    ("mdi:radiator",       "mdi:radiator-off"),
    WARM_WATER_KEY: ("mdi:water-boiler",   "mdi:water-boiler-off"),
    GAS_VALVE_1_KEY: ("mdi:valve-open",   "mdi:valve-closed"),
    GAS_VALVE_2_KEY: ("mdi:valve-open",   "mdi:valve-closed"),
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    async_add_entities([WeishauptBinarySensor(hass, {}, desc) for desc in BINARY_SENSOR_DESCRIPTIONS.values()])


class WeishauptBinarySensor(WeishauptBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, hass, config, description: BinarySensorEntityDescription):
        super().__init__(hass, config)
        self.entity_description = description
        self._attr_unique_id = f"weishaupt_wcm_{description.key.lower().replace(' ', '_')}"

    @property
    def is_on(self) -> bool | None:
        value = self.api().getData().get(self.entity_description.key)
        if value is None:
            return None
        return bool(value)

    @property
    def icon(self) -> str | None:
        icons = _ICONS.get(self.entity_description.key)
        if icons is None:
            return None
        return icons[0] if self.is_on else icons[1]

    async def async_update(self):
        _LOGGER.debug("[async_update] Updating binary sensor: %s", self.entity_description.key)
        await self.hass.async_add_executor_job(super().update)
