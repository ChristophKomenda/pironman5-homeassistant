from homeassistant.components.number import (
    NumberEntity,
    NumberMode,
)

from .const import DOMAIN


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            PironmanRGBSpeed(
                coordinator,
                entry.entry_id,
            )
        ]
    )


class PironmanRGBSpeed(NumberEntity):
    _attr_name = "RGB Effect Speed"
    _attr_has_entity_name = True
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, entry_id):
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry_id}_rgb_speed"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.host)},
            "name": "Pironman 5 Max",
            "manufacturer": "SunFounder",
            "model": "Pironman 5 Max",
        }

    @property
    def native_value(self):
        return self.coordinator.data.get(
            "rgb_speed",
            50,
        )

    async def async_set_native_value(self, value):
        await self.coordinator.post(
            "set-rgb-speed",
            {
                "speed": int(value)
            },
        )
