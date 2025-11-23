"""Sensor platform for Centrometal boiler."""
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .sensor_definitions import ALL_SENSORS, TEMPERATURE_SENSORS, COUNTER_SENSORS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Centrometal sensor entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []

    # Create sensors for all defined parameters
    for param_key, sensor_config in ALL_SENSORS.items():
        sensors.append(
            CentrometalSensor(
                coordinator,
                entry,
                param_key,
                sensor_config,
            )
        )

    # Add status sensor
    sensors.append(CentrometalStatusSensor(coordinator, entry))

    _LOGGER.info("Created %d Centrometal sensors", len(sensors))
    async_add_entities(sensors)


class CentrometalSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Centrometal sensor."""

    def __init__(self, coordinator, entry, param_key, sensor_config):
        """Initialize the sensor."""
        super().__init__(coordinator)

        self._param_key = param_key
        self._sensor_config = sensor_config

        device_id = entry.data.get("device_id", entry.entry_id)

        self._attr_name = f"Centrometal {sensor_config['name']}"
        self._attr_unique_id = f"centrometal_{device_id}_{param_key}"
        self._attr_icon = sensor_config["icon"]
        self._attr_native_unit_of_measurement = sensor_config["unit"]
        self._attr_device_class = sensor_config["device_class"]

        # Set state class based on sensor type
        if param_key in COUNTER_SENSORS:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif sensor_config["device_class"] == SensorDeviceClass.TEMPERATURE:
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif sensor_config["unit"] is not None:
            self._attr_state_class = SensorStateClass.MEASUREMENT
        else:
            self._attr_state_class = None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        value = self.coordinator.data.get(self._param_key)

        if value is None:
            return None

        # Filter out invalid temperature readings (-55 = sensor not connected)
        if self._sensor_config["device_class"] == SensorDeviceClass.TEMPERATURE:
            try:
                if float(value) == -55:
                    return None
            except (ValueError, TypeError):
                pass

        # Convert binary values to ON/OFF for display
        if self._param_key in ["K1B_onOff", "K2B_onOff", "B_P1", "B_P2", "B_P3",
                                "K1B_P", "K2B_P", "B_cm2k", "B_zar", "B_zahP1",
                                "B_zahP2", "B_zahP3"]:
            try:
                return "ON" if int(value) else "OFF"
            except (ValueError, TypeError):
                return value

        return value

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None


class CentrometalStatusSensor(CoordinatorEntity, SensorEntity):
    """Status sensor for Centrometal boiler with comprehensive attributes."""

    _attr_icon = "mdi:information"

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        device_id = entry.data.get("device_id", entry.entry_id)
        self._attr_name = "Centrometal Boiler Status"
        self._attr_unique_id = f"centrometal_{device_id}_status"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return "Unknown"
        return self.coordinator.data.get("B_STATE", "Unknown")

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}

        data = self.coordinator.data
        attributes = {
            "product_name": data.get("B_PRODNAME"),
            "brand": data.get("B_BRAND"),
            "installation": data.get("B_INST"),
            "power": data.get("B_sng"),
            "wifi_version": data.get("B_WifiVER"),
            "firmware_version": data.get("B_VER"),
            "configuration": data.get("B_KONF"),
            "support_type": data.get("B_SUP_TYPE"),
            "circuit1_type": data.get("K1B_CircType"),
            "circuit2_type": data.get("K2B_CircType"),
            "total_parameters": len(data),
        }
        # Remove None values
        return {k: v for k, v in attributes.items() if v is not None}

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None
