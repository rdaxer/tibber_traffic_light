"""Config flow for Tibber Traffic Light."""
import voluptuous as vol
from homeassistant import config_entries
import logging

DOMAIN = "tibber_traffic_light"
_LOGGER = logging.getLogger(__name__)


class TibberTrafficLightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Tibber Traffic Light."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            if user_input.get("price_offset", 20) < 5 or user_input.get("price_offset", 20) > 50:
                errors["base"] = "invalid_offset"
            else:
                return self.async_create_entry(
                    title="Tibber Ampel",
                    data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional("price_offset", default=20): vol.All(
                        vol.Coerce(int), vol.Range(min=5, max=50)
                    ),
                }
            ),
            errors=errors,
        )