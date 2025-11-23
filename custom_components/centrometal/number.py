"""Number platform for Centrometal boiler."""
import logging

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Number definitions (parameter, id, name, description, icon, state_key, min, max, step, unit)
NUMBERS = [
    ("PWR 3", "pwr3", "Boiler Temperature", "Boiler temperature setpoint", "mdi:thermometer", "PVAL_3_0", 75, 90, 1, "°C"),
    ("PWR 10", "pwr10", "DHW Temperature", "Domestic hot water temperature setpoint", "mdi:water-thermometer", "PVAL_10_0", 40, 80, 1, "°C"),
    ("PWR 140", "pwr140", "Day Room Temperature (2nd Circuit)", "Day room temperature setpoint for 2nd circuit", "mdi:home-thermometer", "PVAL_140_0", 5, 30, 0.1, "°C"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Centrometal number entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    numbers = []

    for command, number_id, name, description, icon, state_key, min_value, max_value, step, unit in NUMBERS:
        numbers.append(
            CentrometalNumber(
                coordinator,
                entry,
                command,
                number_id,
                name,
                description,
                icon,
                state_key,
                min_value,
                max_value,
                step,
                unit,
            )
        )

    async_add_entities(numbers)


class CentrometalNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Centrometal number."""

    def __init__(
        self,
        coordinator,
        entry,
        command,
        number_id,
        name,
        description,
        icon,
        state_key,
        min_value,
        max_value,
        step,
        unit,
    ):
        """Initialize the number."""
        super().__init__(coordinator)
        self._command = command
        self._state_key = state_key
        self._attr_name = f"Centrometal {name}"
        self._attr_unique_id = f"centrometal_{entry.data.get('device_id', entry.entry_id)}_{number_id}"
        self._attr_icon = icon
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = unit
        self._attr_has_entity_name = True
        self._entry = entry

    @property
    def native_value(self):
        """Return the current value."""
        value = self.coordinator.data.get(self._state_key)
        if value is None:
            return None
        # Convert to float
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.info("Setting %s to %s (command: %s = %s)", self._attr_name, value, self._command, value)

        # Send command via API
        success = await self.coordinator.api.send_command({self._command: value})

        if success:
            _LOGGER.info("Successfully sent command for %s = %s", self._attr_name, value)
            # Request data refresh to update state
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to send command for %s", self._attr_name)

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success
