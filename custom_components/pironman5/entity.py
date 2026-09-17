from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import PironmanCoordinator


class PironmanEntity(CoordinatorEntity[PironmanCoordinator]):
    """Base entity for Pironman 5."""

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return self.coordinator.device_info
