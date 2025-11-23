"""Config flow for Centrometal integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .api import CentrometalAPI
from .const import DOMAIN, CONF_INSTALL_ID

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_INSTALL_ID, default="1844"): cv.string,
})



class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Centrometal."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Try to login with provided credentials
            api = CentrometalAPI(
                user_input[CONF_EMAIL],
                user_input[CONF_PASSWORD],
                user_input[CONF_INSTALL_ID]
            )

            try:
                if await api.login():
                    await api.close()

                    # Create unique ID from install_id
                    await self.async_set_unique_id(user_input[CONF_INSTALL_ID])
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=f"Centrometal {user_input[CONF_INSTALL_ID]}",
                        data=user_input
                    )
                else:
                    errors["base"] = "auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            finally:
                await api.close()

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors
        )
