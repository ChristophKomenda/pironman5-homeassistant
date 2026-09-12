from homeassistant.components.light import (
    LightEntity,
    ColorMode,
)

from .const import DOMAIN


RGB_STYLES = [
    "solid",
    "breathing",
    "flow",
    "flow_reverse",
    "rainbow",
    "rainbow_reverse",
    "hue_cycle",
]


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            PironmanRGBLight(
                coordinator,
                entry.entry_id,
            )
        ]
    )


class PironmanRGBLight(LightEntity):
    _attr_name = "RGB"
    _attr_has_entity_name = True
    _attr_supported_color_modes = {
        ColorMode.RGB
    }
    _attr_color_mode = ColorMode.RGB
    def __init__(self, coordinator, entry_id):
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry_id}_rgb"

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
            self.coordinator.data.get("rgb_enable", True)
        )

    @property
    def brightness(self):
        brightness = self.coordinator.data.get(
            "rgb_brightness",
            100,
        )
        return round(brightness * 255 / 100)

    @property
    def rgb_color(self):
        color = self.coordinator.data.get(
            "rgb_color",
            "#ffffff",
        )
        color = color.lstrip("#")

        if len(color) != 6:
            return (255, 255, 255)

        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16),
        )

    @property
    def effect_list(self):
        return RGB_STYLES

    @property
    def effect(self):
        return self.coordinator.data.get(
            "rgb_style"
        )

    async def async_turn_on(self, **kwargs):
        await self.coordinator.post(
            "set-rgb-enable",
            {"enable": True},
        )

        if "brightness" in kwargs:
            brightness = round(
                kwargs["brightness"] * 100 / 255
            )

            await self.coordinator.post(
                "set-rgb-brightness",
                {"brightness": brightness},
            )

        if "rgb_color" in kwargs:
            r, g, b = kwargs["rgb_color"]

            color = f"#{r:02x}{g:02x}{b:02x}"

            await self.coordinator.post(
                "set-rgb-color",
                {"color": color},
            )

        if "effect" in kwargs:
            if kwargs["effect"] in RGB_STYLES:
                await self.coordinator.post(
                    "set-rgb-style",
                    {"style": kwargs["effect"]},
                )

    async def async_turn_off(self, **kwargs):
        await self.coordinator.post(
            "set-rgb-enable",
            {"enable": False},
        )
