"""Switch platform for Centrometal boiler."""
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Switch definitions (parameter, name, description, icon)
SWITCHES = [
    ("PWR 99", "pwr99", "1st Heating Circuit", "1st heating circuit control", "mdi:radiator", "PVAL_99_0"),
    ("PWR 129", "pwr129", "2nd Heating Circuit", "2nd heating circuit control", "mdi:radiator", "PVAL_129_0"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Centrometal switch entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    switches = []

    for command, switch_id, name, description, icon, state_key in SWITCHES:
        switches.append(
            CentrometalSwitch(
                coordinator,
                entry,
                command,
                switch_id,
                name,
                description,
                icon,
                state_key,
            )
        )

    async_add_entities(switches)


class CentrometalSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Centrometal switch."""

    def __init__(
        self,
        coordinator,
        entry,
        command,
        switch_id,
        name,
        description,
        icon,
        state_key,
    ):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._command = command
        self._state_key = state_key
        self._attr_name = f"Centrometal {name}"
        self._attr_unique_id = f"centrometal_{entry.data.get('device_id', entry.entry_id)}_{switch_id}"
        self._attr_icon = icon
        self._attr_has_entity_name = True
        self._entry = entry

    @property
    def is_on(self):
        """Return true if switch is on."""
        value = self.coordinator.data.get(self._state_key)
        if value is None:
            return None
        # Convert to int and check if 1
        try:
            return int(value) == 1
        except (ValueError, TypeError):
            return False

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        _LOGGER.info("Turning on %s (command: %s = 1)", self._attr_name, self._command)

        # Send command via API
        success = await self.coordinator.api.send_command({self._command: 1})

        if success:
            _LOGGER.info("Successfully sent ON command for %s", self._attr_name)
            # Request data refresh to update state
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to send ON command for %s", self._attr_name)

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.info("Turning off %s (command: %s = 0)", self._attr_name, self._command)

        # Send command via API
        success = await self.coordinator.api.send_command({self._command: 0})

        if success:
            _LOGGER.info("Successfully sent OFF command for %s", self._attr_name)
            # Request data refresh to update state
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to send OFF command for %s", self._attr_name)

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success
