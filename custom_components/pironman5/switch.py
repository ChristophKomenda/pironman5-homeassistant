from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .coordinator import PironmanCoordinator
from .oled import PironmanOLED


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator: PironmanCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            PironmanOLEDEnabledSwitch(
                coordinator,
                entry.entry_id,
            )
        ]
    )


class PironmanOLEDEnabledSwitch(SwitchEntity):
    """Represent the Pironman OLED enable state."""

    _attr_has_entity_name = True
    _attr_name = "OLED"
    _attr_icon = "mdi:monitor"

    def __init__(
        self,
        coordinator: PironmanCoordinator,
        entry_id: str,
    ) -> None:
        self.coordinator = coordinator
        self.oled = PironmanOLED(coordinator)

        self._attr_unique_id = f"{entry_id}_oled_enabled"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.host)},
            "name": "Pironman 5 Max",
            "manufacturer": "SunFounder",
            "model": "Pironman 5 Max",
        }

    @property
    def is_on(self) -> bool:
        return bool(
            self.coordinator.data.get("oled_enable", False)
        )

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_turn_on(self, **kwargs) -> None:
        await self.oled.set_enabled(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.oled.set_enabled(False)
        await self.coordinator.async_request_refresh()
