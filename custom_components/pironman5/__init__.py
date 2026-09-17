from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import PironmanCoordinator

type PironmanConfigEntry = ConfigEntry[PironmanCoordinator]


PLATFORMS = [
    "sensor",
    "binary_sensor",
    "select",
    "light",
    "number",
    "switch",
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PironmanConfigEntry,
) -> bool:
    """Set up Pironman 5 from a config entry."""
    coordinator = PironmanCoordinator(
        hass,
        entry,
        entry.data["host"],
        entry.data["port"],
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: PironmanConfigEntry,
) -> bool:
    """Unload Pironman 5."""
    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
