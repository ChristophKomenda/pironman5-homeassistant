from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfFrequency,
    UnitOfInformation,
    UnitOfDataRate,
)

from .const import DOMAIN
from .coordinator import PironmanCoordinator


SENSORS = [
    (
        "cpu_temperature",
        "CPU Temperature",
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        "cpu_temperature",
    ),
    (
        "gpu_temperature",
        "GPU Temperature",
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        "gpu_temperature",
    ),
    (
        "cpu_usage",
        "CPU Usage",
        None,
        PERCENTAGE,
        "cpu_percent",
    ),
    (
        "cpu_frequency",
        "CPU Frequency",
        None,
        UnitOfFrequency.MEGAHERTZ,
        "cpu_freq",
    ),
    (
        "memory_usage",
        "Memory Usage",
        None,
        PERCENTAGE,
        "memory_percent",
    ),
    (
        "memory_used",
        "Memory Used",
        SensorDeviceClass.DATA_SIZE,
        UnitOfInformation.BYTES,
        "memory_used",
    ),
    (
        "nvme_usage",
        "NVMe Usage",
        None,
        PERCENTAGE,
        "disk_/dev/nvme0n1_percent",
    ),
    (
        "network_download",
        "Network Download",
        SensorDeviceClass.DATA_RATE,
        UnitOfDataRate.BYTES_PER_SECOND,
        "network_download_speed",
    ),
    (
        "network_upload",
        "Network Upload",
        SensorDeviceClass.DATA_RATE,
        UnitOfDataRate.BYTES_PER_SECOND,
        "network_upload_speed",
    ),
    (
        "fan_speed",
        "Fan Speed",
        None,
        PERCENTAGE,
        "pwm_fan_speed",
    ),
]


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator: PironmanCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for key, name, device_class, unit, data_key in SENSORS:
        entities.append(
            PironmanSensor(
                coordinator,
                entry.entry_id,
                key,
                name,
                device_class,
                unit,
                data_key,
            )
        )

    async_add_entities(entities)


class PironmanSensor(SensorEntity):
    def __init__(
        self,
        coordinator,
        entry_id,
        key,
        name,
        device_class,
        unit,
        data_key,
    ):
        self.coordinator = coordinator
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._data_key = data_key
        self._attr_has_entity_name = True

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
        return self.coordinator.data.get(self._data_key)

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_update(self):
        await self.coordinator.async_request_refresh()
