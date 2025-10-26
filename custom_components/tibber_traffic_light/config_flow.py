"""Config flow for Tibber Traffic Light."""
import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "tibber_traffic_light"


class TibberTrafficLightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Tibber Traffic Light."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(
                title="Tibber Traffic Light",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("price_low", default=0.20): vol.Coerce(float),
                vol.Required("price_high", default=0.30): vol.Coerce(float),
            }),
        )


# Registriere die Config Flow Klasse
CONFIG_FLOW = TibberTrafficLightConfigFlow
