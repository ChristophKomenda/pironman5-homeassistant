"""OLED control for the Pironman 5 integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .coordinator import PironmanCoordinator


class PironmanOLED:
    """Provide a small abstraction for Pironman OLED configuration."""

    def __init__(self, coordinator: PironmanCoordinator) -> None:
        self.coordinator = coordinator

    async def set_enabled(self, enabled: bool):
        """Enable or disable the OLED display."""
        return await self.coordinator.post(
            "set-config",
            {"data": {"system": {"oled_enable": enabled}}},
        )

    async def set_rotation(self, rotation: int):
        """Set OLED rotation."""
        if rotation not in (0, 180):
            raise ValueError("OLED rotation must be 0 or 180")

        return await self.coordinator.post(
            "set-config",
            {"data": {"system": {"oled_rotation": rotation}}},
        )

    async def set_pages(self, pages: list[str]):
        """Set the OLED page sequence."""
        return await self.coordinator.post(
            "set-config",
            {"data": {"system": {"oled_pages": pages}}},
        )

    async def set_sleep_timeout(self, timeout: int):
        """Set the OLED sleep timeout in seconds."""
        if timeout < 0:
            raise ValueError("OLED sleep timeout must be 0 or greater")

        return await self.coordinator.post(
            "set-config",
            {"data": {"system": {"oled_sleep_timeout": timeout}}},
        )
