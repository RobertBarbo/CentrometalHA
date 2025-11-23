"""Climate platform for Centrometal boiler."""
import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Centrometal climate entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([CentrometalClimate(coordinator, entry)])


class CentrometalClimate(CoordinatorEntity, ClimateEntity):
    """Representation of Centrometal boiler as climate device."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
    _attr_supported_features = ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF

    def __init__(self, coordinator, entry):
        """Initialize the climate device."""
        super().__init__(coordinator)
        self._attr_name = f"Centrometal Boiler {entry.data['install_id']}"
        self._attr_unique_id = f"centrometal_{entry.data['install_id']}_climate"
        self._entry = entry

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current operation mode."""
        # Check C1B_onOff or K1B_onOff for boiler circuit state
        # Also check B_STATE for overall boiler state
        circuit_on = self.coordinator.data.get("C1B_onOff") or self.coordinator.data.get("K1B_onOff")
        boiler_state = self.coordinator.data.get("B_STATE", "OFF")

        # If circuit is on or boiler state is not OFF, consider it heating
        if circuit_on == 1 or (boiler_state and boiler_state != "OFF"):
            return HVACMode.HEAT

        return HVACMode.OFF

    @property
    def current_temperature(self):
        """Return the current temperature."""
        # Get boiler temperature from B_Tk1
        return self.coordinator.data.get("B_Tk1")

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVACMode.HEAT:
            await self.coordinator.api.turn_on()
        elif hvac_mode == HVACMode.OFF:
            await self.coordinator.api.turn_off()

        # Request data refresh
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        await self.async_set_hvac_mode(HVACMode.OFF)
