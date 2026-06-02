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
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfVolume,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    OIL_CONSUMPTION_KEY,
    OUTSIDE_TEMPERATURE_KEY,
    WARM_WATER_TEMPERATURE_KEY,
    FLOW_TEMPERATURE_KEY,
    FLUE_GAS_TEMPERATURE_KEY,
    MIXED_EXTERNAL_TEMPERATURE_KEY,
    ROOM_TEMPERATURE_KEY,
    OPERATING_PHASE_KEY,
    ERROR_KEY,
    HEAT_DEMAND_KEY,
    HEATING_SPECIAL_LEVEL_KEY,
    TIME_SINCE_LAST_SERVICE_KEY,
    BURNER_STARTS_KEY,
    BURNER_HOURS_KEY,
    BURNER_LOAD_KEY,
    SYSTEM_FROST_PROTECTION_KEY,
    MIN_FLOW_TEMP_KEY,
    MAX_FLOW_TEMP_KEY,
    FLOW_TEMP_HYSTERESIS_KEY,
    BURNER_LOCKOUT_TIME_KEY,
    MAX_DHW_OUTPUT_KEY,
    MAX_DHW_CHARGE_TIME_KEY,
)
from . import WeishauptBaseEntity

_LOGGER = logging.getLogger(__name__)

SENSOR_DESCRIPTIONS: dict[str, SensorEntityDescription] = {
    # --- Live process temperatures ---
    FLOW_TEMPERATURE_KEY: SensorEntityDescription(
        key=FLOW_TEMPERATURE_KEY,
        translation_key="flow_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    FLUE_GAS_TEMPERATURE_KEY: SensorEntityDescription(
        key=FLUE_GAS_TEMPERATURE_KEY,
        translation_key="flue_gas_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    OUTSIDE_TEMPERATURE_KEY: SensorEntityDescription(
        key=OUTSIDE_TEMPERATURE_KEY,
        translation_key="outside_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    WARM_WATER_TEMPERATURE_KEY: SensorEntityDescription(
        key=WARM_WATER_TEMPERATURE_KEY,
        translation_key="warm_water_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ROOM_TEMPERATURE_KEY: SensorEntityDescription(
        key=ROOM_TEMPERATURE_KEY,
        translation_key="room_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    MIXED_EXTERNAL_TEMPERATURE_KEY: SensorEntityDescription(
        key=MIXED_EXTERNAL_TEMPERATURE_KEY,
        translation_key="mixed_external_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    HEAT_DEMAND_KEY: SensorEntityDescription(
        key=HEAT_DEMAND_KEY,
        translation_key="heat_demand",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    # --- Operating status ---
    OPERATING_PHASE_KEY: SensorEntityDescription(
        key=OPERATING_PHASE_KEY,
        translation_key="operating_phase",
    ),
    BURNER_LOAD_KEY: SensorEntityDescription(
        key=BURNER_LOAD_KEY,
        translation_key="burner_load",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    ERROR_KEY: SensorEntityDescription(
        key=ERROR_KEY,
        translation_key="error",
    ),
    # --- Counters & service ---
    BURNER_STARTS_KEY: SensorEntityDescription(
        key=BURNER_STARTS_KEY,
        translation_key="burner_starts",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    BURNER_HOURS_KEY: SensorEntityDescription(
        key=BURNER_HOURS_KEY,
        translation_key="burner_hours",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.HOURS,
    ),
    TIME_SINCE_LAST_SERVICE_KEY: SensorEntityDescription(
        key=TIME_SINCE_LAST_SERVICE_KEY,
        translation_key="time_since_last_service",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.HOURS,
    ),
    OIL_CONSUMPTION_KEY: SensorEntityDescription(
        key=OIL_CONSUMPTION_KEY,
        translation_key="oil_meter",
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfVolume.LITERS,
    ),
    # --- Configuration setpoints ---
    SYSTEM_FROST_PROTECTION_KEY: SensorEntityDescription(
        key=SYSTEM_FROST_PROTECTION_KEY,
        translation_key="system_frost_protection",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    HEATING_SPECIAL_LEVEL_KEY: SensorEntityDescription(
        key=HEATING_SPECIAL_LEVEL_KEY,
        translation_key="heating_special_level",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    MIN_FLOW_TEMP_KEY: SensorEntityDescription(
        key=MIN_FLOW_TEMP_KEY,
        translation_key="min_flow_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    MAX_FLOW_TEMP_KEY: SensorEntityDescription(
        key=MAX_FLOW_TEMP_KEY,
        translation_key="max_flow_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    FLOW_TEMP_HYSTERESIS_KEY: SensorEntityDescription(
        key=FLOW_TEMP_HYSTERESIS_KEY,
        translation_key="flow_temp_hysteresis",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    BURNER_LOCKOUT_TIME_KEY: SensorEntityDescription(
        key=BURNER_LOCKOUT_TIME_KEY,
        translation_key="burner_lockout_time",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
    MAX_DHW_OUTPUT_KEY: SensorEntityDescription(
        key=MAX_DHW_OUTPUT_KEY,
        translation_key="max_dhw_output",
        native_unit_of_measurement=PERCENTAGE,
    ),
    MAX_DHW_CHARGE_TIME_KEY: SensorEntityDescription(
        key=MAX_DHW_CHARGE_TIME_KEY,
        translation_key="max_dhw_charge_time",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    async_add_entities(_build_entities(hass, {}))


def _build_entities(hass, config):
    return [WeishauptSensor(hass, config, desc) for desc in SENSOR_DESCRIPTIONS.values()]


class WeishauptSensor(WeishauptBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, hass, config, description: SensorEntityDescription):
        super().__init__(hass, config)
        self.entity_description = description
        self._attr_unique_id = f"weishaupt_wcm_{description.key.lower().replace(' ', '_')}"

    @property
    def native_value(self):
        return self.api().getData().get(self.entity_description.key)

    async def async_update(self):
        _LOGGER.debug("[async_update] Updating sensor: %s", self.entity_description.key)
        await self.hass.async_add_executor_job(super().update)
