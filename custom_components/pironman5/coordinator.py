from datetime import timedelta
import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import API_PATH, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class PironmanCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, port):
        self.hass = hass
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}{API_PATH}"
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name="Pironman 5",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        try:
            async with self.session.get(
                f"{self.base_url}/get-data",
                timeout=5,
            ) as response:
                response.raise_for_status()
                data_result = await response.json()

            async with self.session.get(
                f"{self.base_url}/get-config",
                timeout=5,
            ) as response:
                response.raise_for_status()
                config_result = await response.json()

            if not data_result.get("status"):
                raise UpdateFailed(
                    "Pironman API returned status=false for get-data"
                )

            if not config_result.get("status"):
                raise UpdateFailed(
                    "Pironman API returned status=false for get-config"
                )

            data = data_result.get("data", {})
            config = config_result.get("data", {}).get("system", {})

            return {
                **data,
                **config,
            }

        except Exception as err:
            raise UpdateFailed(
                f"Unable to communicate with Pironman API: {err}"
            ) from err

    async def post(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}"

        try:
            async with self.session.post(
                url,
                json=payload,
                timeout=5,
            ) as response:
                response.raise_for_status()
                result = await response.json()

            if not result.get("status"):
                raise UpdateFailed(
                    f"Pironman API rejected request: {result}"
                )

            await self.async_request_refresh()

            return result

        except Exception as err:
            raise UpdateFailed(
                f"Pironman API request failed: {err}"
            ) from err
