"""Tibber Traffic Light Light."""
import logging
from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)
DOMAIN = "tibber_traffic_light"
PRICE_SENSOR = "sensor.keksi_strompreis"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up light."""
    price_low = entry.data.get("price_low", 0.20)
    price_high = entry.data.get("price_high", 0.30)
    light = TibberTrafficLight(hass, price_low, price_high)
    async_add_entities([light])


class TibberTrafficLight(LightEntity):
    """Tibber Traffic Light."""

    _attr_should_poll = False

    def __init__(self, hass, price_low, price_high):
        """Initialize."""
        self.hass = hass
        self._price_low = price_low
        self._price_high = price_high
        self._is_on = True
        self._current_price = 0.0
        self._hs_color = (120, 100)

    @property
    def name(self):
        """Return name."""
        return "Tibber Traffic Light"

    @property
    def unique_id(self):
        """Return unique id."""
        return "tibber_traffic_light"

    @property
    def is_on(self):
        """Return if light is on."""
        return self._is_on

    @property
    def hs_color(self):
        """Return HS color."""
        return self._hs_color

    @property
    def supported_color_modes(self):
        """Return supported color modes."""
        return {"hs"}

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        return {
            "current_price": round(self._current_price, 4),
            "price_low": self._price_low,
            "price_high": self._price_high,
        }

    async def async_turn_on(self, **kwargs):
        """Turn on."""
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off."""
        self._is_on = False
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Added to hass."""
        await self._update_price()
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [PRICE_SENSOR], self._on_price_change
            )
        )

    @callback
    def _on_price_change(self, event):
        """Price changed."""
        self.hass.async_create_task(self._update_price())

    async def _update_price(self):
        """Update price and color."""
        state = self.hass.states.get(PRICE_SENSOR)
        if not state or state.state in ("unknown", "unavailable"):
            return

        try:
            self._current_price = float(state.state)
            self._update_color()
        except (ValueError, TypeError):
            _LOGGER.error("Cannot convert price to float")

    def _update_color(self):
        """Update color."""
        if self._current_price < self._price_low:
            self._hs_color = (120, 100)  # Green
        elif self._current_price > self._price_high:
            self._hs_color = (0, 100)  # Red
        else:
            self._hs_color = (60, 100)  # Yellow

        self.async_write_ha_state()
