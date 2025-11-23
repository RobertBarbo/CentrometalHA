"""Sensor platform for Centrometal boiler."""
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Temperature sensors definition
TEMPERATURE_SENSORS = [
    ("boiler_temperature", "Boiler Temperature", "B_Tk1"),
    ("hot_water_temperature", "Hot Water Temperature", "B_Tptv1"),
    ("outdoor_temperature", "Outdoor Temperature", "B_Tva1"),
    ("buffer_tank_up", "Buffer Tank Up", "B_Tak1"),
    ("buffer_tank_down", "Buffer Tank Down", "B_Tak2"),
    ("flue_gas_temperature", "Flue Gas Temperature", "B_Tdpl1"),
    ("hydraulic_crossover", "Hydraulic Crossover", "B_Ths1"),
    ("mixer_temperature", "Mixer Temperature", "B_Tpov1"),
    ("low_temp_sensor", "Low Temperature Sensor", "B_Tlo1"),
    ("circuit1_temperature", "Circuit 1 Temperature", "C1B_Tpol1"),
    ("circuit1_temperature_alt", "Circuit 1 Temperature Alt", "C1B_Tpol"),
    ("circuit2_temperature", "Circuit 2 Temperature", "C2B_Tpol1"),
    ("circuit2_temperature_alt", "Circuit 2 Temperature Alt", "C2B_Tpol"),
    ("circuit1_room_temp", "Circuit 1 Room Temp", "C1B_Tsob1"),
    ("circuit1_room_temp_alt", "Circuit 1 Room Temp Alt", "C1B_Tsob"),
    ("circuit2_room_temp", "Circuit 2 Room Temp", "C2B_Tsob1"),
    ("circuit2_room_temp_alt", "Circuit 2 Room Temp Alt", "C2B_Tsob"),
]

# Percentage sensors
PERCENTAGE_SENSORS = [
    ("oxygen_level", "Oxygen Level", "B_Oxy1", "mdi:molecule"),
]

# Binary state sensors (0/1)
BINARY_STATE_SENSORS = [
    ("fan_state", "Fan State", "B_fan", "mdi:fan"),
    ("heater_state", "Heater State", "B_gri", "mdi:fire"),
    ("boiler_pump", "Boiler Pump", "B_Pk", "mdi:pump"),
    ("pellet_transporter", "Pellet Transporter", "B_puz", "mdi:grain"),
    ("circuit1_on_off", "Circuit 1 ON/OFF", "C1B_onOff", "mdi:heating-coil"),
    ("circuit2_on_off", "Circuit 2 ON/OFF", "C2B_onOff", "mdi:heating-coil"),
    ("boiler_operational", "Boiler Operational", "B_uklKot", "mdi:power"),
    ("freeze_guard", "Freeze Guard", "B_freezEn", "mdi:snowflake-alert"),
    ("remote_start_enabled", "Remote Start Enabled", "B_netMon", "mdi:lan"),
    ("circuit1_pump", "Circuit 1 Pump", "C1B_P", "mdi:pump"),
    ("circuit2_pump", "Circuit 2 Pump", "C2B_P", "mdi:pump"),
    ("circuit1_day_night", "Circuit 1 Day/Night", "C1B_dayNight", "mdi:weather-night"),
    ("circuit2_day_night", "Circuit 2 Day/Night", "C2B_dayNight", "mdi:weather-night"),
]

# Counter sensors
COUNTER_SENSORS = [
    ("cnt_burner_work", "Burner Work Time", "CNT_0", "mdi:fire-circle"),
    ("cnt_dhw_only", "DHW Only Time", "CNT_1", "mdi:water-boiler"),
    ("cnt_freeze_protection", "Freeze Protection Time", "CNT_2", "mdi:snowflake"),
    ("cnt_burner_starts", "Burner Start Count", "CNT_3", "mdi:counter"),
    ("cnt_fan_work", "Fan Work Time", "CNT_4", "mdi:fan-clock"),
    ("cnt_electric_heater_work", "Electric Heater Work Time", "CNT_5", "mdi:radiator"),
    ("cnt_electric_heater_starts", "Electric Heater Starts", "CNT_6", "mdi:counter"),
    ("cnt_vacuum_turbine", "Vacuum Turbine Work Time", "CNT_7", "mdi:turbine"),
    ("cnt_boiler_pump", "Boiler Pump Work Time", "CNT_8", "mdi:pump-off"),
    ("cnt_9", "Counter 9", "CNT_9", "mdi:counter"),
    ("cnt_10", "Counter 10", "CNT_10", "mdi:counter"),
    ("cnt_11", "Counter 11", "CNT_11", "mdi:counter"),
    ("cnt_12", "Counter 12", "CNT_12", "mdi:counter"),
    ("cnt_13", "Counter 13", "CNT_13", "mdi:counter"),
    ("cnt_14", "Counter 14", "CNT_14", "mdi:counter"),
    ("cnt_15", "Counter 15", "CNT_15", "mdi:counter"),
]

# Numeric sensors (non-temperature)
NUMERIC_SENSORS = [
    ("pellet_tank_level", "Pellet Tank Level", "B_cmsr100", PERCENTAGE, "mdi:gauge"),
    ("fire_sensor", "Fire Sensor", "B_FotV", None, "mdi:fire-alert"),
    ("mixing_valve", "Mixing Valve", "B_misP", PERCENTAGE, "mdi:valve"),
    ("circuit1_correction", "Circuit 1 Correction", "C1B_kor", "°C", "mdi:thermometer"),
    ("circuit2_correction", "Circuit 2 Correction", "C2B_kor", "°C", "mdi:thermometer"),
    ("pellet_on_time", "Pellet Transporter On", "B_puzOn", "s", "mdi:timer"),
    ("pellet_off_time", "Pellet Transporter Off", "B_puzOff", "s", "mdi:timer-off"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Centrometal sensor entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []

    # Add all temperature sensors
    for sensor_id, name, data_key in TEMPERATURE_SENSORS:
        sensors.append(
            CentrometalTemperatureSensor(coordinator, entry, sensor_id, name, data_key)
        )

    # Add percentage sensors
    for sensor_id, name, data_key, icon in PERCENTAGE_SENSORS:
        sensors.append(
            CentrometalPercentageSensor(coordinator, entry, sensor_id, name, data_key, icon)
        )

    # Add binary state sensors
    for sensor_id, name, data_key, icon in BINARY_STATE_SENSORS:
        sensors.append(
            CentrometalBinaryStateSensor(coordinator, entry, sensor_id, name, data_key, icon)
        )

    # Add counter sensors
    for sensor_id, name, data_key, icon in COUNTER_SENSORS:
        sensors.append(
            CentrometalCounterSensor(coordinator, entry, sensor_id, name, data_key, icon)
        )

    # Add numeric sensors
    for sensor_id, name, data_key, unit, icon in NUMERIC_SENSORS:
        sensors.append(
            CentrometalNumericSensor(coordinator, entry, sensor_id, name, data_key, unit, icon)
        )

    # Add special status sensor with attributes
    sensors.append(CentrometalStatusSensor(coordinator, entry))

    async_add_entities(sensors)


class CentrometalTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Temperature sensor for Centrometal boiler."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, entry, sensor_id, name, data_key):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"Centrometal {name}"
        self._attr_unique_id = f"centrometal_{entry.data['install_id']}_{sensor_id}"
        self._data_key = data_key

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._data_key)


class CentrometalPercentageSensor(CoordinatorEntity, SensorEntity):
    """Percentage sensor for Centrometal boiler."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator, entry, sensor_id, name, data_key, icon):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"Centrometal {name}"
        self._attr_unique_id = f"centrometal_{entry.data['install_id']}_{sensor_id}"
        self._attr_icon = icon
        self._data_key = data_key

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._data_key)


class CentrometalBinaryStateSensor(CoordinatorEntity, SensorEntity):
    """Binary state sensor (0/1) for Centrometal boiler."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry, sensor_id, name, data_key, icon):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"Centrometal {name}"
        self._attr_unique_id = f"centrometal_{entry.data['install_id']}_{sensor_id}"
        self._attr_icon = icon
        self._data_key = data_key

    @property
    def native_value(self):
        """Return the state of the sensor."""
        value = self.coordinator.data.get(self._data_key)
        # Return as string "ON" or "OFF" for better display
        if value is None:
            return None
        # Fan can have numeric values (RPM), others are 0/1
        if self._data_key == "B_fan" and isinstance(value, (int, float)) and value > 100:
            return value  # Return RPM value
        return "ON" if value else "OFF"


class CentrometalCounterSensor(CoordinatorEntity, SensorEntity):
    """Counter sensor for Centrometal boiler."""

    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, coordinator, entry, sensor_id, name, data_key, icon):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"Centrometal {name}"
        self._attr_unique_id = f"centrometal_{entry.data['install_id']}_{sensor_id}"
        self._attr_icon = icon
        self._data_key = data_key

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._data_key)


class CentrometalNumericSensor(CoordinatorEntity, SensorEntity):
    """Numeric sensor for Centrometal boiler."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry, sensor_id, name, data_key, unit, icon):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"Centrometal {name}"
        self._attr_unique_id = f"centrometal_{entry.data['install_id']}_{sensor_id}"
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit
        self._data_key = data_key

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._data_key)


class CentrometalStatusSensor(CoordinatorEntity, SensorEntity):
    """Status sensor for Centrometal boiler with comprehensive attributes."""

    _attr_icon = "mdi:information"

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Centrometal Boiler Status"
        self._attr_unique_id = f"centrometal_{entry.data['install_id']}_status"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("B_STATE", "Unknown")

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        data = self.coordinator.data
        attributes = {
            "product_name": data.get("B_PRODNAME"),
            "brand": data.get("B_BRAND"),
            "power": data.get("B_sng"),
            "wifi_version": data.get("B_WifiVER"),
            "firmware_version": data.get("B_VER"),
            "installation": data.get("B_INST"),
            "configuration": data.get("B_KONF"),
            "configuration_string": data.get("B_KONF_STR"),
            "command_active": data.get("B_CMD"),
            "operation_mode": data.get("B_zlj"),
            "additional_features": data.get("B_Add"),
            "accessories": data.get("B_AddConf"),
            "sup_type": data.get("B_SUP_TYPE"),
            "time": data.get("B_Time"),
        }
        # Remove None values
        return {k: v for k, v in attributes.items() if v is not None}
