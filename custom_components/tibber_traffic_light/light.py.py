"""Tibber Traffic Light - nutzt existierende Sensoren."""
import logging

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tibber_traffic_light"
CURRENT_PRICE_SENSOR = "sensor.keksi_strompreis"
AVERAGE_PRICE_SENSOR = "sensor.tibber_average_price"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Tibber Traffic Light."""
    price_offset = entry.data.get("price_offset", 20)

    light = TibberTrafficLight(hass, price_offset)
    async_add_entities([light])


class TibberTrafficLight(LightEntity):
    """Tibber Traffic Light Entity."""

    def __init__(self, hass, price_offset):
        """Initialize the light."""
        self.hass = hass
        self._price_offset = price_offset
        self._is_on = True
        self._current_price = 0
        self._average_price = 0
        self._hs_color = (120, 100)  # Standard: Grün
        self._brightness = 255
        self._attr_should_poll = False

    @property
    def name(self):
        """Return the name of the light."""
        return "Tibber Traffic Light"

    @property
    def unique_id(self):
        """Return unique ID."""
        return "tibber_traffic_light_main"

    @property
    def is_on(self):
        """Return True if light is on."""
        return self._is_on

    @property
    def brightness(self):
        """Return brightness."""
        return self._brightness

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
        """Return extra state attributes."""
        lower = self._average_price * (1 - self._price_offset / 100)
        upper = self._average_price * (1 + self._price_offset / 100)

        return {
            "current_price": round(self._current_price, 4),
            "average_price": round(self._average_price, 4),
            "price_status": self._get_price_status(),
            "lower_limit": round(lower, 4),
            "upper_limit": round(upper, 4),
            "price_offset": self._price_offset,
        }

    def _get_price_status(self):
        """Get price status as string."""
        if self._average_price == 0:
            return "Keine Daten"

        lower = self._average_price * (1 - self._price_offset / 100)
        upper = self._average_price * (1 + self._price_offset / 100)

        if self._current_price < lower:
            return "Günstig (Grün) 🟢"
        elif self._current_price > upper:
            return "Teuer (Rot) 🔴"
        else:
            return "Durchschnitt (Gelb) 🟡"

    async def async_turn_on(self, **kwargs):
        """Turn on the light."""
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the light."""
        self._is_on = False
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        # Initiales Update
        await self._update_from_sensors()

        # Tracker für State-Changes
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [CURRENT_PRICE_SENSOR, AVERAGE_PRICE_SENSOR],
                self._on_sensor_change,
            )
        )

    @callback
    def _on_sensor_change(self, event):
        """Handle sensor state changes."""
        self.hass.async_create_task(self._update_from_sensors())

    async def _update_from_sensors(self):
        """Update light state from sensors."""
        try:
            # Aktuellen Preis abrufen
            current = self.hass.states.get(CURRENT_PRICE_SENSOR)
            if current and current.state not in ("unknown", "unavailable"):
                self._current_price = float(current.state)

            # Durchschnittspreis abrufen
            average = self.hass.states.get(AVERAGE_PRICE_SENSOR)
            if average and average.state not in ("unknown", "unavailable"):
                self._average_price = float(average.state)

            # Farbe aktualisieren
            self._update_color()

            _LOGGER.debug(
                "Updated - Current: %s, Average: %s, Status: %s",
                self._current_price,
                self._average_price,
                self._get_price_status(),
            )

        except (ValueError, TypeError) as err:
            _LOGGER.error("Error updating sensors: %s", err)

    def _update_color(self):
        """Update color based on price."""
        if self._average_price == 0:
            self._hs_color = (120, 100)  # Grün als Default
            self.async_write_ha_state()
            return

        lower = self._average_price * (1 - self._price_offset / 100)
        upper = self._average_price * (1 + self._price_offset / 100)

        if self._current_price < lower:
            # Grün: Hue 120°
            self._hs_color = (120, 100)
        elif self._current_price > upper:
            # Rot: Hue 0°
            self._hs_color = (0, 100)
        else:
            # Gelb: Hue 60°
            self._hs_color = (60, 100)

        self.async_write_ha_state()