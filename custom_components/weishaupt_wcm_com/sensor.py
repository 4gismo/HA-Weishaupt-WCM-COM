"""Platform for sensor integration."""
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPower,
    UnitOfVolume,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, NAME_PREFIX
from .const import (
    OIL_CONSUMPTION_KEY,
    OUTSIDE_TEMPERATURE_KEY,
    LOAD_SETTING_KEY,
    WARM_WATER_TEMPERATURE_KEY,
    FLOW_TEMPERATURE_KEY,
    FLUE_GAS_TEMPERATURE_KEY,
    MIXED_EXTERNAL_TEMPERATURE_KEY,
    ROOM_TEMPERATURE_KEY,
    OPERATING_MODE_KEY,
    OPERATING_PHASE_KEY,
    PUMP_KEY,
    WARM_WATER_KEY,
    FLAME_KEY,
    ERROR_KEY,
    GAS_VALVE_1_KEY,
    GAS_VALVE_2_KEY,
    HEATING_KEY,
    HEAT_DEMAND_KEY,
    BUFFER_SENSOR_B10_KEY,
    TIME_SINCE_LAST_SERVICE_KEY,
    DAMPED_OUTSIDE_TEMPERATURE_KEY,
    BURNER_STARTS_KEY,
    BURNER_HOURS_KEY,
)
from . import WeishauptBaseEntity

_LOGGER = logging.getLogger(__name__)

SENSOR_DESCRIPTIONS: dict[str, SensorEntityDescription] = {
    OIL_CONSUMPTION_KEY: SensorEntityDescription(
        key=OIL_CONSUMPTION_KEY,
        name="Oil Meter",
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfVolume.LITERS,
    ),
    OUTSIDE_TEMPERATURE_KEY: SensorEntityDescription(
        key=OUTSIDE_TEMPERATURE_KEY,
        name="Outside Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    LOAD_SETTING_KEY: SensorEntityDescription(
        key=LOAD_SETTING_KEY,
        name="Load Setting",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
    ),
    WARM_WATER_TEMPERATURE_KEY: SensorEntityDescription(
        key=WARM_WATER_TEMPERATURE_KEY,
        name="Warm Water Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    FLOW_TEMPERATURE_KEY: SensorEntityDescription(
        key=FLOW_TEMPERATURE_KEY,
        name="Flow Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    FLUE_GAS_TEMPERATURE_KEY: SensorEntityDescription(
        key=FLUE_GAS_TEMPERATURE_KEY,
        name="Flue Gas Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ROOM_TEMPERATURE_KEY: SensorEntityDescription(
        key=ROOM_TEMPERATURE_KEY,
        name="Room Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    MIXED_EXTERNAL_TEMPERATURE_KEY: SensorEntityDescription(
        key=MIXED_EXTERNAL_TEMPERATURE_KEY,
        name="Mixed External Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    OPERATING_MODE_KEY: SensorEntityDescription(
        key=OPERATING_MODE_KEY,
        name="Operating Mode",
    ),
    OPERATING_PHASE_KEY: SensorEntityDescription(
        key=OPERATING_PHASE_KEY,
        name="Operating Phase",
    ),
    PUMP_KEY: SensorEntityDescription(
        key=PUMP_KEY,
        name="Pump",
    ),
    WARM_WATER_KEY: SensorEntityDescription(
        key=WARM_WATER_KEY,
        name="Warm Water",
    ),
    FLAME_KEY: SensorEntityDescription(
        key=FLAME_KEY,
        name="Flame",
    ),
    ERROR_KEY: SensorEntityDescription(
        key=ERROR_KEY,
        name="Error",
    ),
    GAS_VALVE_1_KEY: SensorEntityDescription(
        key=GAS_VALVE_1_KEY,
        name="Gas Valve 1",
    ),
    GAS_VALVE_2_KEY: SensorEntityDescription(
        key=GAS_VALVE_2_KEY,
        name="Gas Valve 2",
    ),
    HEATING_KEY: SensorEntityDescription(
        key=HEATING_KEY,
        name="Heating",
    ),
    HEAT_DEMAND_KEY: SensorEntityDescription(
        key=HEAT_DEMAND_KEY,
        name="Heat Demand",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    BUFFER_SENSOR_B10_KEY: SensorEntityDescription(
        key=BUFFER_SENSOR_B10_KEY,
        name="Buffer Sensor B10",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    TIME_SINCE_LAST_SERVICE_KEY: SensorEntityDescription(
        key=TIME_SINCE_LAST_SERVICE_KEY,
        name="Time Since Last Service",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.HOURS,
    ),
    DAMPED_OUTSIDE_TEMPERATURE_KEY: SensorEntityDescription(
        key=DAMPED_OUTSIDE_TEMPERATURE_KEY,
        name="Damped Outside Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    BURNER_STARTS_KEY: SensorEntityDescription(
        key=BURNER_STARTS_KEY,
        name="Burner Starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BURNER_HOURS_KEY: SensorEntityDescription(
        key=BURNER_HOURS_KEY,
        name="Burner Hours",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.HOURS,
    ),
}


def setup_platform(hass, config, add_entities, discovery_info=None):
    if discovery_info is None:
        return
    add_entities(_build_entities(hass, config))


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    async_add_entities(_build_entities(hass, {}))


def _build_entities(hass, config):
    return [WeishauptSensor(hass, config, desc) for desc in SENSOR_DESCRIPTIONS.values()]


class WeishauptSensor(WeishauptBaseEntity, SensorEntity):

    def __init__(self, hass, config, description: SensorEntityDescription):
        super().__init__(hass, config)
        self.entity_description = description
        self._attr_unique_id = f"weishaupt_wcm_{description.key.lower().replace(' ', '_')}"

    @property
    def name(self):
        return NAME_PREFIX + self.entity_description.name

    @property
    def native_value(self):
        return self.api().getData().get(self.entity_description.key)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "weishaupt_wcm")},
            "name": "Weishaupt WCM-COM",
            "manufacturer": "Weishaupt",
            "model": "WCM-COM",
            "configuration_url": f"http://{self.api()._host}/",
        }

    async def async_update(self):
        _LOGGER.debug("[async_update] Updating sensor: %s", self.entity_description.key)
        await self.hass.async_add_executor_job(super().update)
