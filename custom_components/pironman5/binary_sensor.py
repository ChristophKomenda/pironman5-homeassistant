from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
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
            PironmanFanState(
                coordinator,
                entry.entry_id,
            )
        ]
    )


class PironmanFanState(BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_name = "Fan Running"
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry_id):
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry_id}_fan_running"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.host)},
            "name": "Pironman 5 Max",
            "manufacturer": "SunFounder",
            "model": "Pironman 5 Max",
        }

    @property
    def is_on(self):
        return bool(
            self.coordinator.data.get("gpio_fan_state", 0)
        )

    @property
    def available(self):
        return self.coordinator.last_update_success
