from homeassistant.components.switch import SwitchEntity

from .entity import PironmanEntity
from .oled import PironmanOLED


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = entry.runtime_data

    async_add_entities(
        [
            PironmanOLEDEnabledSwitch(
                coordinator,
                entry.entry_id,
            )
        ]
    )


class PironmanOLEDEnabledSwitch(
    PironmanEntity,
    SwitchEntity,
):
    _attr_has_entity_name = True
    _attr_name = "OLED"
    _attr_icon = "mdi:monitor"

    def __init__(
        self,
        coordinator,
        entry_id,
    ) -> None:
        super().__init__(coordinator)

        self.oled = PironmanOLED(coordinator)

        self._attr_unique_id = f"{entry_id}_oled_enabled"

    @property
    def is_on(self) -> bool:
        return bool(
            self.coordinator.data.get(
                "oled_enable",
                False,
            )
        )

    async def async_turn_on(
        self,
        **kwargs,
    ) -> None:
        await self.oled.set_enabled(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(
        self,
        **kwargs,
    ) -> None:
        await self.oled.set_enabled(False)
        await self.coordinator.async_request_refresh()
