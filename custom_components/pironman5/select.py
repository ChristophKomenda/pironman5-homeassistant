from homeassistant.components.select import SelectEntity

from .const import DOMAIN


FAN_MODES = {
    "Always On": 0,
    "Performance": 1,
    "Cool": 2,
    "Balanced": 3,
    "Quiet": 4,
}


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            PironmanFanMode(
                coordinator,
                entry.entry_id,
            )
        ]
    )


class PironmanFanMode(SelectEntity):
    _attr_name = "Fan Mode"
    _attr_has_entity_name = True
    _attr_options = list(FAN_MODES.keys())

    def __init__(self, coordinator, entry_id):
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry_id}_fan_mode"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.host)},
            "name": "Pironman 5 Max",
            "manufacturer": "SunFounder",
            "model": "Pironman 5 Max",
        }

    @property
    def current_option(self):
        mode = self.coordinator.data.get("gpio_fan_mode")

        reverse = {
            value: key
            for key, value in FAN_MODES.items()
        }

        return reverse.get(mode)

    async def async_select_option(self, option):
        await self.coordinator.post(
            "set-fan-mode",
            {
                "fan_mode": FAN_MODES[option]
            },
        )
