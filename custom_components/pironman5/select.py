from homeassistant.components.select import SelectEntity

from .const import DOMAIN
from .oled import PironmanOLED


FAN_MODES = {
    "Always On": 0,
    "Performance": 1,
    "Cool": 2,
    "Balanced": 3,
    "Quiet": 4,
}


GPIO_FAN_LED_MODES = {
    "On": "on",
    "Off": "off",
    "Follow": "follow",
}


OLED_PAGES = {
    "Mix": "mix",
    "Performance": "performance",
    "IPs": "ips",
    "Disk": "disk",
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
            ),
            PironmanGPIOFanLED(
                coordinator,
                entry.entry_id,
            ),
            PironmanOLEDRotation(
                coordinator,
                entry.entry_id,
            ),
            PironmanOLEDPage(
                coordinator,
                entry.entry_id,
            ),
        ]
    )


class PironmanFanMode(SelectEntity):
    """Represent the Pironman fan mode."""

    _attr_name = "Fan Mode"
    _attr_has_entity_name = True
    _attr_options = list(FAN_MODES.keys())

    def __init__(
        self,
        coordinator,
        entry_id,
    ):
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
                "fan_mode": FAN_MODES[option],
            },
        )


class PironmanGPIOFanLED(SelectEntity):
    """Represent the GPIO fan LED."""

    _attr_name = "GPIO Fan LED"
    _attr_has_entity_name = True
    _attr_options = list(GPIO_FAN_LED_MODES.keys())
    _attr_icon = "mdi:led-on"

    def __init__(
        self,
        coordinator,
        entry_id,
    ):
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry_id}_gpio_fan_led"

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
        led = self.coordinator.data.get("gpio_fan_led")

        reverse = {
            value: key
            for key, value in GPIO_FAN_LED_MODES.items()
        }

        return reverse.get(led)

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_select_option(self, option):
        await self.coordinator.post(
            "set-fan-led",
            {
                "led": GPIO_FAN_LED_MODES[option],
            },
        )


class PironmanOLEDRotation(SelectEntity):
    """Represent the Pironman OLED rotation."""

    _attr_name = "OLED Rotation"
    _attr_has_entity_name = True
    _attr_options = ["0°", "180°"]
    _attr_icon = "mdi:rotate-3d-variant"

    def __init__(
        self,
        coordinator,
        entry_id,
    ):
        self.coordinator = coordinator
        self.oled = PironmanOLED(coordinator)
        self._attr_unique_id = f"{entry_id}_oled_rotation"

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
        rotation = self.coordinator.data.get(
            "oled_rotation",
            0,
        )

        return f"{rotation}°"

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_select_option(self, option):
        await self.oled.set_rotation(
            int(option.rstrip("°"))
        )

        await self.coordinator.async_request_refresh()


class PironmanOLEDPage(SelectEntity):
    """Represent the primary Pironman OLED page."""

    _attr_name = "OLED Page"
    _attr_has_entity_name = True
    _attr_options = list(OLED_PAGES.keys())
    _attr_icon = "mdi:monitor-dashboard"

    def __init__(
        self,
        coordinator,
        entry_id,
    ):
        self.coordinator = coordinator
        self.oled = PironmanOLED(coordinator)
        self._attr_unique_id = f"{entry_id}_oled_page"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.host)},
            "name": "Pironman 5 Max",
            "manufacturer": "SunFounder",
            "model": "Pironman 5 Max",
        }

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def current_option(self):
        pages = self.coordinator.data.get(
            "oled_pages",
            [
                "mix",
                "performance",
                "ips",
                "disk",
            ],
        )

        if not pages:
            return None

        page = pages[0]

        reverse = {
            value: key
            for key, value in OLED_PAGES.items()
        }

        return reverse.get(page)

    async def async_select_option(self, option):
        pages = list(
            self.coordinator.data.get(
                "oled_pages",
                [
                    "mix",
                    "performance",
                    "ips",
                    "disk",
                ],
            )
        )

        if not pages:
            pages = [
                "mix",
                "performance",
                "ips",
                "disk",
            ]

        pages[0] = OLED_PAGES[option]

        await self.oled.set_pages(pages)

        await self.coordinator.async_request_refresh()
